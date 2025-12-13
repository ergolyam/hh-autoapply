from worker.config.config import Config


async def post_vacancy(page) -> bool:
    await page.locator('div.vacancy-actions [data-qa="vacancy-response-link-top"]').first.click()

    try:
        await page.locator('[data-qa="relocation-warning-confirm"]').wait_for(state="visible", timeout=3000).click()
    except:
        pass

    try:
        await page.get_by_text("Для отклика необходимо ответить", exact=False).first.wait_for(state="visible", timeout=3000)
        return False
    except:
        pass

    await page.locator('[data-qa="textarea-native-wrapper"] textarea').fill(Config.letter_input)

    await page.locator('[data-qa="vacancy-response-letter-submit"]').click()

    return True


if __name__ == '__main__':
    raise RuntimeError('This module should be run only via main.py')
