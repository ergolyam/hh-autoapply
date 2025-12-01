from worker.api.get_vacancies import vacancies_request
from worker.core.helpers import Common
from worker.funcs.chatbot import VacancyBot
from worker.api.ntfysh import send_notify
from worker.db.vacancies import add_vac, get_vac


async def process_vacancy(vac, bot):
    vid = vac['id']
    
    existing = await get_vac(vid)
    if existing['status'] is not None:
        print(f'Vacancy {vid} already in DB. Skipping.')
        return

    print(f'Processing {vid}...')
    
    bot_msg = f'''
    name: {vac['name']}\n
    requirement: {vac['requirement']}\n
    responsibility: {vac['responsibility']}\n
    description: {vac['description']}
    '''
    
    await bot.run_bot(bot_msg)
    result = bot.show_agent_result()
    selection = bot.show_selection()

    await add_vac(vac_id=vid, status=selection, cause=result)
    print(f'Saved {vid} to DB (Status: {selection})')

    ntfy_title = f'[{vid}]: {vac['name']}'
    ntfy_msg = f'''
    llm selected: {selection}
    llm commented: {result}
    '''
    await send_notify(
        title=ntfy_title,
        text=ntfy_msg,
        click=vac['url']
    )


async def cycle_responses():
    bot = VacancyBot()
    bot.set_filter_phrase(Common.cfg['input']['filter_phrase'])

    first_page = await vacancies_request()

    total_pages = first_page[0]['pages']
    total_vacancies = first_page[0]['total']
    total_pages_msg = f'Total pages: {total_pages}\nTotal vacancies: {total_vacancies}'
    print(total_pages_msg)
    
    await send_notify(
        title='Responses have started!',
        text=total_pages_msg
    )

    page_msg = f'Page 0|{total_pages}'
    print(page_msg)
    await send_notify(text=page_msg)

    for vac in first_page[1:]:
        await process_vacancy(vac, bot)

    for page in range(1, total_pages):
        vacancies = await vacancies_request(page=page)

        page_msg = f'Page {page}|{total_pages}'
        print(page_msg)
        await send_notify(text=page_msg)
        
        for vac in vacancies[1:]:
            await process_vacancy(vac, bot)


if __name__ == '__main__':
    raise RuntimeError('This module should be run only via main.py')
