from worker.core.logs import Log
from worker.config.config import settings


async def post_vacancy(page, url = None) -> bool:
    if url:
        Log.log.info(f'Navigating to {url}')
        await page.goto(url, wait_until='domcontentloaded')

        title = await page.locator('[data-qa="vacancy-title"]').inner_text()
        Log.log.info(f'Vacancy: {title}')

    try:
        await page.locator('div.vacancy-actions [data-qa="vacancy-response-link-top"]').first.click()
    except:
        return False

    try:
        await page.locator('[data-qa="relocation-warning-confirm"]').click(timeout=3000)
    except:
        pass

    try:
        await page.get_by_text('Для отклика необходимо ответить', exact=False).first.wait_for(state='visible', timeout=3000)
        return False
    except:
        pass

    await page.locator('[data-qa="textarea-native-wrapper"] textarea').fill(settings.letter_input)

    await page.locator('[data-qa="vacancy-response-letter-submit"], [data-qa="vacancy-response-submit-popup"]').click()

    return True


if __name__ == '__main__':
    raise RuntimeError('This module should be run only via main.py')
