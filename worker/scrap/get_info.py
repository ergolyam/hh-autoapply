from worker.config.config import Config
from worker.api.ntfy_img import send_notify_image


async def get_user(page):
    url = f'https://{Config.hh_domain}/applicant/resumes'
    print(f'Navigating to {url}...')
    await page.goto(url)

    name_locator = page.locator('[data-qa="cell-text-content"]').first

    name = (await name_locator.inner_text() or '').strip()

    print(f'Name on the resume page: {name}')

    await send_notify_image(page, title='Resumes page')


if __name__ == '__main__':
    raise RuntimeError('This module should be run only via main.py')
