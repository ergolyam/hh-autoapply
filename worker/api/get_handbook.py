from worker.api.base import request

async def handbook_request(topic: str | None) -> list:
    resp = await request('dictionaries')
    if resp.get('ok', False):
        data = resp.get('data', {})
        if not topic:
             return list(data.keys())
        return data.get(topic, [])
    else:
        raise Exception(f'Error {resp.get('status_code', None)}: {resp.get('details', None)}')


if __name__ == '__main__':
    raise RuntimeError('This module should be run only via main.py')
