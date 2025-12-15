from worker.config.config import settings
from worker.core.helpers import Log
from worker.scrap.get_vacancies import get_vacancies
from worker.scrap.get_vacancy import get_vacancy
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
        vac_info = await get_vacancy(page, vurl)
        
        bot_msg = f'''
        name: {vac_info['name']}\n
        experience: {vac_info['experience']}\n
        employment: {vac_info['employment']}\n
        schedule: {vac_info['schedule']}\n
        work_format: {vac_info['work_format']}\n
        salary: {vac_info['salary']}\n
        description: {vac_info['description']}\n
        skills: {vac_info['skills']}
        '''
        
        Log.log.info(f'Processing with GPT Bot...')
        await bot.run_bot(bot_msg)
        result = bot.show_agent_result()
        selection = bot.show_selection()
        ntfy_title = f'[{vid}]: {vac_info['name']}'
        ntfy_msg = f'''
        llm selected: {selection}
        llm commented: {result}
        '''

        access = True
        if selection:
            Log.log.info('Response to vacancy...')
            access = await post_vacancy(page)
        if not access:
            ntfy_msg = 'Unable to respond to the vacancy.'
            selection = False
            Log.log.error(ntfy_msg)
            await send_notify_image(
                page,
                filename='not_access.png',
                title=ntfy_title,
                message=ntfy_msg,
                click=vurl
            )
        else:
            await send_notify(
                title=ntfy_title,
                text=ntfy_msg,
                click=vurl
            )

        await add_vac(vac_id=vid, status=selection, cause=result)
        Log.log.info(f'Saved vacancy to DB (Status: {selection})')


async def cycle_responses(page):
    bot = VacancyBot()
    bot.set_filter_phrase(settings.filter_phrase)

    page_index = 0
    while True:
        vacancies_data = await get_vacancies(page, page_index=page_index, search_text=settings.search_text)
        count = vacancies_data.get('count')
        if not count:
            msg = f'All pages are clicked through.'
            await send_notify(text=msg)
            Log.log.warning(msg)
            break

        vacancies = vacancies_data['index']
        await send_notify(title=f'Page {page_index}', text=f'Found {count} vacancies.')
        
        for vac in vacancies[1:]:
            await process_vacancy(page, vac, bot)

        page_index = page_index + 1


if __name__ == '__main__':
    raise RuntimeError('This module should be run only via main.py')
