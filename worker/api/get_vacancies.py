from worker.api.base import request
from worker.core.helpers import Common


async def vacancy_detals(id: int):
    resp = await request(f'vacancies/{id}')
    if resp.get('ok', False):
        data = resp.get('data', [])
        return data
    else:
        raise Exception(f'Error {resp.get('status_code', None)}: {resp.get('details', None)}')


def drop_none(d: dict) -> dict:
    return {k: v for k, v in d.items() if v not in (None, 'None')}


async def vacancies_request(resume_id: str, page: int = 0):
    params = drop_none({
        'page': page,
        'per_page': 10,
        'text': Common.cfg['vacancies']['text'],
        'experience': Common.cfg['vacancies']['experience'],
        'employment': Common.cfg['vacancies']['employment'],
        'schedule': Common.cfg['vacancies']['schedule'],
        'salary': Common.cfg['vacancies']['salary']
    })
    resp = await request(
        path=f'resumes/{resume_id}/similar_vacancies',
        params=params
    )
    if resp.get('ok', False):
        data = resp.get('data', {})
        items = data.get('items', {})
        vacancies = []
        vacancies.append({'pages': data.get('pages')})
        for item in items:
            snippet = item.get('snippet', {})
            salary = item.get('salary', {})
            vid = item.get('id')
            description = await vacancy_detals(vid)
            vacancy = {
                'id': vid,
                'name': item.get('name'),
                'url': item.get('alternate_url'),
                'requirement': snippet.get('requirement'),
                'responsibility': snippet.get('responsibility'),
                'description': description.get('description'),
                'salary': f'{salary.get('from') if salary else 0} {salary.get('currency') if salary else 'Null'}'
            }
            vacancies.append(vacancy)
        return vacancies
    else:
        raise Exception(f'Error {resp.get('status_code', None)}: {resp.get('details', None)}')


if __name__ == '__main__':
    raise RuntimeError('This module should be run only via main.py')
