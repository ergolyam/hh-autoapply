from urllib.parse import urlparse, quote_plus
from worker.config.config import settings
from worker.core.helpers import Log


async def get_vacancies(page, search_text: str, page_index: int = 0) -> dict:
    search = quote_plus(search_text)
    url = (
        f'https://{settings.hh_domain}/search/vacancy'
        f'?text={search}&page={page_index}'
    )
    Log.log.info(f'Navigating to {url}')
    response = await page.goto(url)
    if response and response.status == 404:
        Log.log.warning(f'Page {page_index} does not exist ({response.status})')
        return {}

    vacancy_links = page.locator('a[data-qa="serp-item__title"]')
    count = await vacancy_links.count()

    vacancies = {
        'count': count,
        'index': []
    }

    for i in range(count):
        vacancy_link = vacancy_links.nth(i)

        title_locator = vacancy_link.locator('[data-qa="serp-item__title-text"]')

        title = (await title_locator.inner_text() or '').strip()
        link = await vacancy_link.get_attribute('href')

        if link and link.startswith('/'):
            link = f'https://{settings.hh_domain}{link}'

        vacancy_id = urlparse(link).path.strip("/").split("/")[-1]

        if title and link:
            vacancies['index'].append({
                'id': vacancy_id,
                'title': title,
                'link': link,
            })

    return vacancies


if __name__ == '__main__':
    raise RuntimeError('This module should be run only via main.py')
