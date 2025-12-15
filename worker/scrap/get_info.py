from worker.config.config import settings
from worker.core.helpers import Log
from worker.api.ntfy_img import send_notify_image


async def get_user(page):
    url = f'https://{settings.hh_domain}/applicant/resumes'
    Log.log.info(f'Navigating to {url}')
    await page.goto(url)

    name_locator = page.locator('[data-qa="cell-text-content"]').first
    await name_locator.wait_for(state='visible', timeout=3000)

    name = (await name_locator.inner_text() or '').strip()

    Log.log.info(f'Name on the resume page: {name}')

    await send_notify_image(page, title='Resumes page')


if __name__ == '__main__':
    raise RuntimeError('This module should be run only via main.py')
