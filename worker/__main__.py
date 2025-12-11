import os, sys, asyncio
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from worker.core.browser import init_browser
from worker.funcs.login import prepare_page
from worker.funcs.get_info import get_user


async def main():
    try:
        browser, page, playwright = await init_browser()
        print('Browser launched successfully')
        await prepare_page(page)
        await get_user(page)
        await browser.close()
        await playwright.stop()
    except Exception as e:
        print(f'An error occurred: {e}')


if __name__ == '__main__':
    asyncio.run(main())
