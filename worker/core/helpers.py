import os

async def take_screenshot(page, file_name):
    print(f'Taking screenshot: {file_name}')
    await page.screenshot(path=file_name)
    print(f'Screenshot saved as {file_name}')
    os.system(f'imv {file_name}')

if __name__ == '__main__':
    raise RuntimeError('This module should be run only via main.py')
