import re
from worker.core.helpers import Log
from worker.core.browser import optional_inner_text

def clean_text(text: str) -> str:
    return re.sub(r'\s+', ' ', text).strip()


async def get_vacancy(page, url) -> dict:
    Log.log.info(f'Navigating to {url}')
    await page.goto(url, wait_until='domcontentloaded')

    title = await page.locator('[data-qa="vacancy-title"]').inner_text()

    experience = await page.locator('[data-qa="vacancy-experience"]').inner_text()

    employment = await page.locator('[data-qa="common-employment-text"], [data-qa="vacancy-view-employment-mode"]').inner_text()

    schedule = await optional_inner_text(page.locator('[data-qa="work-schedule-by-days-text"]'))

    work_format = await optional_inner_text(page.locator('[data-qa="work-formats-text"]'))

    salary = await optional_inner_text(page.locator('[data-qa="vacancy-salary"]'))

    descriptions = await page.locator('[data-qa="vacancy-description"]').all_inner_texts()
    if not descriptions:
        raise ValueError('vacancy-description not found')
    description = ' '.join(descriptions)

    skills = await page.locator('[data-qa="skills-element"] div').all_inner_texts()

    return {
        'name': title,
        'experience': experience,
        'employment': employment,
        'schedule': clean_text(schedule),
        'work_format': clean_text(work_format),
        'salary': clean_text(salary),
        'description': clean_text(description),
        'skills': clean_text(', '.join(skills))
    }


if __name__ == '__main__':
    raise RuntimeError('This module should be run only via main.py')
