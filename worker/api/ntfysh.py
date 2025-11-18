from worker.core.helpers import Common
from worker.config.config import Config

async def send_notify(text: str, title: str = '', click: str = ''):
    url = f'{Config.ntfy_url}/{Config.ntfy_topic}'

    kargs: dict = {
        'url': url,
        'content': text.encode(encoding='utf-8')
    }

    if title or click:
        kargs.setdefault('headers', {})

    if title:
        kargs['headers']['Title'] = title.encode(encoding='utf-8')

    if click:
        kargs['headers']['Click'] = click

    response = await Common.http.post(**kargs)
    if response.status_code == 200:
        return

    try:
        err = response.json()
        details = err.get('description') or err.get('error') or err
    except Exception:
        details = response.text
    raise Exception(f'Error {response.status_code}: {details}')

if __name__ == '__main__':
    raise RuntimeError('This module should be run only via main.py')
