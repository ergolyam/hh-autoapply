from worker.config.config import Config


async def post_vacancy(page):
    await page.locator('div.vacancy-actions [data-qa="vacancy-response-link-top"]').first.click()

    try:
        await page.locator('[data-qa="relocation-warning-confirm"]').click()
    except:
        pass

    await page.locator('[data-qa="textarea-native-wrapper"] textarea').fill(Config.letter_input)

    await page.locator('[data-qa="vacancy-response-letter-submit"]').click()


if __name__ == '__main__':
    raise RuntimeError('This module should be run only via main.py')
