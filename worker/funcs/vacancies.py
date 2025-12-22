from worker.config.config import settings
from worker.core.helpers import Common
from worker.core.logs import Log
from worker.api.get_vacancies import vacancies_request, vacancy_detals
from worker.scrap.post_vacancy import post_vacancy
from worker.funcs.chatbot import VacancyBot
from worker.api.ntfy_msg import send_notify
from worker.api.ntfy_img import send_notify_image
from worker.db.vacancies import add_vac, get_vac


async def process_vacancy(page, vac, bot):
    vid = vac['id']
    vurl = vac['link']

    with Log.vacancy(vid):
        existing = await get_vac(vid)
        if existing['status'] is not None:
            Log.log.warning(f'Vacancy already in DB. Skipping.')
            return

        Log.log.info(f'Processing vacancy...')
        vac_info = await vacancy_detals(vid)
        bot_msg = f'''
name: {vac['name']}\n
description: {vac_info['description']}\n
salary: {vac['salary']}\n
        '''
        
        Log.log.info(f'Processing with GPT Bot...')
        await bot.run_bot(bot_msg)
        result = bot.show_agent_result()
        selection = bot.show_selection()
        emoji_str = '🟢' if selection else '🔴'
        ntfy_title = f'({emoji_str})[{vid}]: {vac['name']}'
        ntfy_msg = f'''
llm selected: {selection} {emoji_str}
llm commented: {result}
        '''

        access = True
        if selection:
            Log.log.info('Response to vacancy...')
            async with Common.post_timer:
                access = await post_vacancy(page, url=vurl)
        if not access:
            ntfy_msg = 'Unable to respond to the vacancy.'
            selection = False
            Log.log.error(ntfy_msg)
            await send_notify_image(
                page,
                filename='not_access.png',
                title=ntfy_title,
                message=ntfy_msg,
                click=vurl,
                priority='high',
                extra_topic='access'
            )
        else:
            await send_notify(
                title=ntfy_title,
                text=ntfy_msg,
                click=vurl,
                extra_topic=str(selection)
            )

        await add_vac(vac_id=vid, status=selection)
        Log.log.info(f'Saved vacancy to DB (Status: {selection})')


async def cycle_responses(page):
    if settings.ntfy_suffix:
        topics = [ 'true', 'false', 'access', 'error' ]
        await send_notify(
            title='Separate topics mode enabled',
            text=(
                'Available topics:\n' + '\n'.join(
                    f'{settings.ntfy_url}/{settings.ntfy_topic}-{topic}' for topic in topics
                )
            )
        )

    bot = VacancyBot()
    bot.set_filter_phrase(settings.filter_phrase)

    page_index = 0
    count = 0
    max_pages = None
    while True:
        if max_pages is not None and page_index >= max_pages:
            msg = 'All vacancies on the accessible pages have been reviewed.'
            await send_notify(text=msg)
            Log.log.warning(msg)
            break

        async with Common.api_timer:
            vacancies_data = await vacancies_request(page=page_index)
        vacancies = vacancies_data['items']
        total = vacancies_data['total']
        max_pages = vacancies_data['pages']

        if not len(vacancies):
            msg = f'All vacancies on the accessible pages have been reviewed.'
            await send_notify(text=msg)
            Log.log.warning(msg)
            break

        count = count + len(vacancies)

        Log.log.info(f'Found {count}/{total} vacancies on page {page_index}/{max_pages}')
        await send_notify(
            title=f'Page {page_index}/{max_pages}',
            text=(f'Found {count}/{total} vacancies.\nSearch Index: {settings.search_text}')
        )
        
        for vac in vacancies:
            await process_vacancy(page, vac, bot)

        page_index = page_index + 1


if __name__ == '__main__':
    raise RuntimeError('This module should be run only via main.py')
