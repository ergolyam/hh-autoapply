from worker.core.helpers import Common
from worker.config.config import settings


async def send_notify(
        text: str,
        title: str = '',
        click: str = '',
        priority: str = '',
        extra_topic: str = ''
):
    url = f'{settings.ntfy_url}/{settings.ntfy_topic}'
    if settings.ntfy_suffix and extra_topic:
        url = url + f'-{extra_topic.lower()}'

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

    if priority:
        kargs['headers']['Priority'] = priority

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
