import os, sys, asyncio, signal, contextlib
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
from worker.core.logs import Log


async def main():
    context = None
    playwright = None
    db_initialized = False
    page = None
    cycle_task = None

    loop = asyncio.get_running_loop()
    stop = loop.create_future()

    def _request_shutdown(signame: str):
        Log.log.info(f'Got {signame}. Shutting down...')
        if not stop.done():
            stop.set_result(None)

    for sig in (signal.SIGINT, signal.SIGTERM):
        try:
            loop.add_signal_handler(sig, _request_shutdown, sig.name)
        except NotImplementedError:
            signal.signal(sig, lambda *_: _request_shutdown(sig.name))

    try:
        browser, playwright = await init_browser()
        Log.log.info('Browser launched successfully')
        state_file = f'{settings.data_path}/{settings.email}.json'
        Path(settings.data_path).mkdir(parents=True, exist_ok=True)
        if Path(state_file).exists():
            context = await browser.new_context(storage_state=state_file)
            page = await context.new_page()
            await init_llm()
            await init_db()
            db_initialized = True
            await get_user(page)
            if '--recovery' in sys.argv:
                from worker.funcs.negotiations import cycle_negotiations
                cycle_task = asyncio.create_task(cycle_negotiations(page), name='cycle_negotiations')
            else: 
                cycle_task = asyncio.create_task(cycle_responses(page), name='cycle_responses')
            done, pending = await asyncio.wait(
                {cycle_task, stop},
                return_when=asyncio.FIRST_COMPLETED
            )
            if cycle_task.done():
                await cycle_task
            elif stop.done():
                Log.log.info('Cancelling responses...')
                cycle_task.cancel()
                with contextlib.suppress(asyncio.CancelledError):
                    await cycle_task
        else:
            context = await browser.new_context()
            page = await context.new_page()
            await prepare_page(page)
            await context.storage_state(path=state_file)
            Log.log.info(f'Auth state saved to: {state_file}')
            await get_user(page)
    except Exception:
        Log.log.exception(f'An error occurred')
        if page:
            await send_notify_image(
                page,
                filename='error.png',
                title='Playwright error',
                priority='max',
                extra_topic='error'
            )
    finally:
        if cycle_task and not cycle_task.done():
            cycle_task.cancel()
            with contextlib.suppress(asyncio.CancelledError):
                await cycle_task
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
    asyncio.run(main())
