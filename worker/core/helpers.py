import httpx, io

async def take_screenshot(page, *, full_page: bool = False, img_type: str = "png") -> io.BytesIO:
    data: bytes = await page.screenshot(full_page=full_page, type=img_type)
    return io.BytesIO(data)

class Common():
    client_timeout = httpx.Timeout(30.0)
    http = httpx.AsyncClient(timeout=client_timeout)


if __name__ == '__main__':
    raise RuntimeError('This module should be run only via main.py')
