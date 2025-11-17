from worker.api.get_vacancies import vacancies_request
from worker.core.helpers import Common
from worker.funcs.chatbot import VacancyBot


async def cycle_responses():
    bot = VacancyBot()
    bot.set_filter_phrase(Common.cfg['input']['filter_phrase'])
    page = 0

    first_page = await vacancies_request(
        resume_id=Common.cfg['settings']['resume_id'],
        page=page
    )

    total_pages = first_page[0]['pages']
    print(f'Total pages: {total_pages}')

    print('Page 0:')
    for vac in first_page[1:]:
        print(vac['id'])
        await bot.run_bot(f'name: {vac['name']}\nrequirement: {vac['requirement']}\nresponsibility: {vac['responsibility']}\ndescription: {vac['description']}')
        bot.show_agent_result()
        bot.show_selection()

    for page in range(1, total_pages):
        vacancies = await vacancies_request(
            resume_id=Common.cfg['settings']['resume_id'],
            page=page
        )

        print(f'\nPage {page}:')
        for vac in vacancies[1:]:
            print(vac['id'])
            await bot.run_bot(f'name: {vac['name']}\nrequirement: {vac['requirement']}\nresponsibility: {vac['responsibility']}\ndescription: {vac['description']}')
            bot.show_agent_result()
            bot.show_selection()


if __name__ == '__main__':
    raise RuntimeError('This module should be run only via main.py')
