from worker.config.config import Config
from worker.scrap.get_vacancies import get_vacancies
from worker.scrap.get_vacancy import get_vacancy
from worker.funcs.chatbot import VacancyBot
from worker.api.ntfy_msg import send_notify
from worker.db.vacancies import add_vac, get_vac


async def process_vacancy(page, vac, bot):
    vid = vac['id']
    vurl = vac['link']
    
    existing = await get_vac(vid)
    if existing['status'] is not None:
        print(f'Vacancy {vid} already in DB. Skipping.')
        return

    print(f'Processing {vid}...')

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
    
    await bot.run_bot(bot_msg)
    result = bot.show_agent_result()
    selection = bot.show_selection()

    await add_vac(vac_id=vid, status=selection, cause=result)
    print(f'Saved {vid} to DB (Status: {selection})')

    ntfy_title = f'[{vid}]: {vac_info['name']}'
    ntfy_msg = f'''
    llm selected: {selection}
    llm commented: {result}
    '''
    await send_notify(
        title=ntfy_title,
        text=ntfy_msg,
        click=vac['link']
    )


async def cycle_responses(page):
    bot = VacancyBot()
    bot.set_filter_phrase(Config.filter_phrase)

    await send_notify(text='Responses have started!')

    page_index = 0
    while True:
        vacancies = await get_vacancies(page, page_index=page_index, search_text=Config.search_text)
        if not vacancies:
            msg = f'All pages are clicked through.'
            await send_notify(text=msg)
            print(msg)
            break

        await send_notify(title='Page', text=str(page_index))
        
        for vac in vacancies[1:]:
            await process_vacancy(page, vac, bot)

        page_index = page_index + 1


if __name__ == '__main__':
    raise RuntimeError('This module should be run only via main.py')
