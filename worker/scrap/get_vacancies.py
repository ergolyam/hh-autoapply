from worker.config.config import Config


async def get_vacancies(page, search_text: str, page_index: int = 0):
    url = (
        f'https://{Config.hh_domain}/search/vacancy'
        f'?text={search_text}&page={page_index}'
    )
    print(f'Navigating to {url}...')
    response = await page.goto(url, wait_until='load')
    if response and response.status == 404:
        print(f'Page {page_index} does not exist ({response.status})')
        return []

    vacancies = []

    vacancy_links = page.locator('a[data-qa="serp-item__title"]')
    count = await vacancy_links.count()

    print(f'Found {count} vacancies on page {page_index}')

    for i in range(count):
        vacancy_link = vacancy_links.nth(i)

        title_locator = vacancy_link.locator('[data-qa="serp-item__title-text"]')

        title = (await title_locator.inner_text() or '').strip()
        link = await vacancy_link.get_attribute('href')

        if link and link.startswith('/'):
            link = f'https://{Config.hh_domain}{link}'

        if title and link:
            vacancies.append({
                'title': title,
                'link': link,
            })

    return vacancies


if __name__ == '__main__':
    raise RuntimeError('This module should be run only via main.py')
