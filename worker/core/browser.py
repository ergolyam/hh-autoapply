from playwright.async_api import async_playwright
from playwright.async_api import TimeoutError as PlaywrightTimeoutError
from worker.config.config import settings


async def init_browser():
    playwright = await async_playwright().start()
    browser = await playwright.chromium.launch(executable_path=settings.chrome_path)
    return browser, playwright


async def optional_inner_text(locator, default='', timeout=3000):
    try:
        await locator.wait_for(state='visible', timeout=timeout)
        return (await locator.inner_text())
    except PlaywrightTimeoutError:
        return default


if __name__ == '__main__':
    raise RuntimeError('This module should be run only via main.py')
