from worker.api.base import request
from worker.config.config import settings

async def vacancy_detals(id: int):
    resp = await request(f'vacancies/{id}')
    if resp.get('ok', False):
        data = resp.get('data', [])
        return {
            'description': data['description']
        }
    else:
        raise Exception(f'Error {resp.get('status_code', None)}: {resp.get('details', None)}')


async def vacancies_request(page: int = 0):
    params = {
        'page': page,
        'per_page': 50,
        'text': settings.search_text,
    }
    resp = await request(
        path=f'vacancies',
        params=params
    )
    if resp.get('ok', False):
        data = resp.get('data', {})
        items = data.get('items', {})
        vacancies = []
        for item in items:
            salary = item.get('salary', {})
            vid = item.get('id')
            vacancy = {
                'id': vid,
                'name': item['name'],
                'link': item['alternate_url'],
                'salary': f'{salary.get('from') if salary else 0} {salary.get('currency') if salary else 'Null'}'
            }
            vacancies.append(vacancy)
        return vacancies
    else:
        raise Exception(f'Error {resp.get('status_code', None)}: {resp.get('details', None)}')


if __name__ == '__main__':
    raise RuntimeError('This module should be run only via main.py')
