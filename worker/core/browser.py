from playwright.async_api import async_playwright
from worker.config.config import Config


async def init_browser():
    playwright = await async_playwright().start()
    browser = await playwright.chromium.launch(executable_path=Config.chrome_path)
    return browser, playwright


if __name__ == '__main__':
    raise RuntimeError('This module should be run only via main.py')
