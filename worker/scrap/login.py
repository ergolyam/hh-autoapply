from worker.config.config import Config
from worker.api.ntfy_img import send_notify_image


async def prepare_page(page, state_file):
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
        msg = 'Capcha is detect!'
        print(msg)
        await send_notify_image(page, filename='capcha.png', title=msg, message='Please prove you are not a robot.')
        capcha_text = input('Enter the text from the image: ')
        await captcha_locator.fill(capcha_text)
        await page.locator('button:has-text("Отправить")').click()

    code = input('Code: ')

    await page.locator('[data-qa="applicant-login-input-otp"]').fill(code)

    await page.context.storage_state(path=state_file)
    print(f'Auth state saved to: {state_file}')


if __name__ == '__main__':
    raise RuntimeError('This module should be run only via main.py')
