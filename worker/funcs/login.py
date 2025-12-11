from worker.core.helpers import take_screenshot
from worker.config.config import Config


async def prepare_page(page):
    print(f'Navigating to {Config.hh_domain}...')
    await page.goto(f'https://{Config.hh_domain}', wait_until='load')

    async with page.expect_navigation(wait_until='load'):
        await page.locator('[data-qa="login"]').click()

    await page.locator('[data-qa="submit-button"]').click()

    await page.get_by_text('Почта', exact=True).click()

    await page.locator('[data-qa="applicant-login-input-email"]').fill(Config.email)

    await page.locator('[data-qa="submit-button"]').click()

    captcha_locator = page.locator('[data-qa="account-captcha-input"]')

    if await captcha_locator.is_visible():
        print('Capcha is detect!')
        await take_screenshot(page, '/tmp/test.jpg')
        capcha_text = input('Enter the text from the image: ')
        await captcha_locator.fill(capcha_text)
        await page.locator('button:has-text("Отправить")').click()

    code = input('Code: ')

    await page.locator('[data-qa="applicant-login-input-otp"]').fill(code)

    await take_screenshot(page, '/tmp/test.jpg')


if __name__ == '__main__':
    raise RuntimeError('This module should be run only via main.py')
