from worker.api.base import request


async def vacancy_detals(id: int):
    resp = await request(f'vacancies/{id}')
    if resp.get('ok', False):
        data = resp.get('data', [])
        return data
    else:
        raise Exception(f'Error {resp.get('status_code', None)}: {resp.get('details', None)}')


async def vacancies_request(resume_id: str, page: int = 0):
    resp = await request(
        path=f'resumes/{resume_id}/similar_vacancies',
        params={'page': 0, 'per_page': 10}
    )
    if resp.get('ok', False):
        data = resp.get('data', {})
        items = data.get('items', {})
        vacancies = []
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
