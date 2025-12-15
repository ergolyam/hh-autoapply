import re
from worker.core.helpers import Log

def clean_text(text: str) -> str:
    return re.sub(r'\s+', ' ', text).strip()


async def get_vacancy(page, url) -> dict:
    Log.log.info(f'Navigating to {url}')
    await page.goto(url)

    title = await page.locator('[data-qa="vacancy-title"]').inner_text()

    experience = await page.locator('[data-qa="vacancy-experience"]').inner_text()

    employment = await page.locator('[data-qa="common-employment-text"], [data-qa="vacancy-view-employment-mode"]').inner_text()

    schedule = page.locator('[data-qa="work-schedule-by-days-text"]')
    if await schedule.count() > 0:
        schedule = await schedule.inner_text()
    else:
        schedule = ''

    work_format = page.locator('[data-qa="work-formats-text"]')
    if await work_format.count() > 0:
        work_format = await work_format.inner_text()
    else:
        work_format = ''

    salary = page.locator('[data-qa="vacancy-salary"]')
    if await salary.count() > 0:
        salary = await salary.inner_text()
    else:
        salary = ''

    descriptions = await page.locator('[data-qa="vacancy-description"]').all_inner_texts()
    description = ' '.join(descriptions)

    skills = await page.locator('[data-qa="skills-element"] div').all_inner_texts()

    return {
        'name': title,
        'experience': experience,
        'employment': employment,
        'schedule': schedule,
        'work_format': clean_text(work_format),
        'salary': clean_text(salary),
        'description': description,
        'skills': clean_text(', '.join(skills))
    }


if __name__ == '__main__':
    raise RuntimeError('This module should be run only via main.py')
