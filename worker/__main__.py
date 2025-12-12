import os, sys, asyncio
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from worker.core.browser import init_browser
from worker.api.ntfy_img import send_notify_image
from worker.scrap.login import prepare_page
from worker.scrap.get_info import get_user
from worker.scrap.get_vacancies import get_vacancies
from worker.config.config import Config


async def main():
    browser = None
    playwright = None
    page = None
    try:
        browser, playwright = await init_browser()
        print('Browser launched successfully')
        if os.path.exists(Config.state_path):
            context = await browser.new_context(storage_state=Config.state_path)
            page = await context.new_page()
            await get_user(page)
            vacancies = await get_vacancies(page, search_text='devops', page_index=0)
            print(vacancies)
        else:
            context = await browser.new_context()
            page = await context.new_page()
            await prepare_page(page)
    except Exception as e:
        msg = f'An error occurred: {e}'
        print(msg)
        assert page
        await send_notify_image(page, filename='error.png', message=msg)
    finally:
        assert browser
        await browser.close()
        assert playwright
        await playwright.stop()


if __name__ == '__main__':
    asyncio.run(main())
