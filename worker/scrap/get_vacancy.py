import re
from worker.core.helpers import Log
from worker.core.browser import optional_inner_text

def clean_text(text: str) -> str:
    return re.sub(r'\s+', ' ', text).strip()


async def get_vacancy(page, url) -> dict:
    Log.log.info(f'Navigating to {url}')
    await page.goto(url, wait_until='domcontentloaded')

    title = await page.locator('[data-qa="vacancy-title"]').inner_text()

    salary = await optional_inner_text(page.locator('[data-qa="vacancy-salary"]'))

    descriptions = await page.locator('[data-qa="vacancy-description"]').all_inner_texts()
    if not descriptions:
        raise ValueError('vacancy-description not found')
    description = ' '.join(descriptions)

    return {
        'name': title,
        'description': description.replace('\xa0', ' ').strip(),
        'salary': clean_text(salary),
    }


if __name__ == '__main__':
    raise RuntimeError('This module should be run only via main.py')
