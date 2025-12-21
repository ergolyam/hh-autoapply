from worker.core.logs import Log
from worker.scrap.get_negotiations import get_negotiations
from worker.db.vacancies import add_vac


async def cycle_negotiations(page):
    page_index = 0
    count = 0
    while True:
        negotiations_data = await get_negotiations(page, page_index)

        negotiations = negotiations_data['items']
        count = count + negotiations_data['count']
        if not negotiations_data['count']:
            msg = f'All pages are added to DB.'
            Log.log.warning(msg)
            break

        Log.log.info(f'Found {count} negotiations on page {page_index}')

        for n in negotiations:
            await add_vac(n, True)
            Log.log.info(f'Saved vacancy [{n}] to DB')

        page_index = page_index + 1


if __name__ == '__main__':
    raise RuntimeError('This module should be run only via main.py')

