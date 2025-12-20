from urllib.parse import urlparse
from worker.config.config import settings
from worker.core.logs import Log


async def get_negotiations(page, page_index: int = 0) -> dict:
    url = f'https://{settings.hh_domain}/applicant/negotiations?page={page_index}'
    
    Log.log.info(f'Navigating to {url}')
    response = await page.goto(url)
    if response and response.status == 404:
        Log.log.warning(f'Page {page_index} does not exist ({response.status})')
        return {}

    items = page.locator('[data-qa="negotiations-item"]')
    count = await items.count()

    negotiations = {
        'count': count,
        'items': []
    }

    for i in range(count):
        item = items.nth(i)

        negotiation_link = item.locator('a[href*="/vacancy/"]').first
        link = await negotiation_link.get_attribute('href')

        negotiation_id = urlparse(link).path.strip('/').split('/')[-1]

        if negotiation_id:
            negotiations['items'].append(negotiation_id)

    return negotiations


if __name__ == '__main__':
    raise RuntimeError('This module should be run only via main.py')
