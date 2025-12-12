from worker.config.config import Config


async def get_user(page):
    url = f'https://{Config.hh_domain}/applicant/resumes'
    print(f'Navigating to {url}...')
    await page.goto(url, wait_until='load')

    name_locator = page.locator('[data-qa="cell-text-content"]').first

    name = (await name_locator.inner_text() or '').strip()

    print(f'Name on the resume page: {name}')


if __name__ == '__main__':
    raise RuntimeError('This module should be run only via main.py')
