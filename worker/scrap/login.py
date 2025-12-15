from worker.config.config import settings
from worker.core.helpers import Log
from worker.api.ntfy_img import send_notify_image


async def prepare_page(page):
    Log.log.info(f'Navigating to {settings.hh_domain}')
    await page.goto(f'https://{settings.hh_domain}')

    await page.locator('[data-qa="login"]').click()

    await page.locator('[data-qa="submit-button"]').click()

    await page.get_by_text('Почта', exact=True).click()

    await page.locator('[data-qa="applicant-login-input-email"]').fill(settings.email)

    await page.locator('[data-qa="submit-button"]').click()

    captcha_locator = page.locator('[data-qa="account-captcha-input"]')

    if await captcha_locator.is_visible():
        msg = 'Capcha is detect!'
        Log.log.warning(msg)
        await send_notify_image(page, filename='capcha.png', title=msg, message='Please prove you are not a robot.')
        capcha_text = Log.console.input('[bright_red]Enter the text from the image:[/] ')
        await captcha_locator.fill(capcha_text)
        await page.locator('button:has-text("Отправить")').click()

    code = Log.console.input('[green3]Enter the code from email:[/] ')

    await page.locator('[data-qa="applicant-login-input-otp"]').fill(code)


if __name__ == '__main__':
    raise RuntimeError('This module should be run only via main.py')
