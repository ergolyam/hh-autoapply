import os, sys, asyncio
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from worker.core.browser import init_browser
from worker.funcs.login import prepare_page
from worker.funcs.get_info import get_user
from worker.config.config import Config


async def main():
    try:
        browser, playwright = await init_browser()
        print('Browser launched successfully')
        if os.path.exists(Config.state_path):
            context = await browser.new_context(storage_state=Config.state_path)
            page = await context.new_page()
            await get_user(page)
        else:
            context = await browser.new_context()
            page = await context.new_page()
            await prepare_page(page)
        await browser.close()
        await playwright.stop()
    except Exception as e:
        print(f'An error occurred: {e}')


if __name__ == '__main__':
    asyncio.run(main())
