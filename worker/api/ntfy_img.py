import io

from worker.core.helpers import Common, take_screenshot
from worker.config.config import Config


async def send_notify_image(
    page,
    filename: str = 'screenshot.png',
    message: str = '',
    title: str = '',
    click: str = '',
    content_type: str = 'image/png',
):
    image = await take_screenshot(page)
    url = f'{Config.ntfy_url}/{Config.ntfy_topic}'

    if isinstance(image, io.BytesIO):
        image_bytes = image.getvalue()
    else:
        image_bytes = image

    headers: dict = {
        'Filename': filename,
        'Content-Type': content_type,
    }

    if message:
        headers['Message'] = message.encode(encoding='utf-8')

    if title:
        headers['Title'] = title.encode(encoding='utf-8')

    if click:
        headers['Click'] = click

    response = await Common.http.put(url=url, content=image_bytes, headers=headers)
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
