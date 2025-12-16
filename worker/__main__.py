import os, sys, asyncio
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from pathlib import Path

from worker.core.browser import init_browser
from worker.api.ntfy_img import send_notify_image
from worker.scrap.login import prepare_page
from worker.scrap.get_info import get_user
from worker.funcs.vacancies import cycle_responses
from worker.core.llm import init_llm
from worker.db.db import init as init_db
from worker.db.db import close as close_db
from worker.config.config import settings
from worker.core.helpers import Log, block_heavy_resources


async def main():
    context = None
    playwright = None
    db_initialized = False
    page = None
    try:
        browser, playwright = await init_browser()
        Log.log.info('Browser launched successfully')
        state_file = f'{settings.state_path}/{settings.email}.json'
        Path(settings.state_path).mkdir(parents=True, exist_ok=True)
        if Path(state_file).exists():
            context = await browser.new_context(storage_state=state_file)
            await block_heavy_resources(context)
            page = await context.new_page()
            await init_llm()
            await init_db()
            db_initialized = True
            await get_user(page)
            await cycle_responses(page)
        else:
            context = await browser.new_context()
            await block_heavy_resources(context)
            page = await context.new_page()
            await prepare_page(page)
            await context.storage_state(path=state_file)
            Log.log.info(f'Auth state saved to: {state_file}')
            await get_user(page)
    except Exception:
        Log.log.exception(f'An error occurred')
        if page:
            await send_notify_image(page, filename='error.png', title='Playwright error')
    finally:
        if context:
            try:
                await context.close()
            except Exception:
                pass
        if playwright:
            try:
                await playwright.stop()
            except Exception:
                pass
        if db_initialized:
            try:
                await close_db()
            except Exception:
                pass


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        Log.log.info('Interrupted by user. Bye!')
