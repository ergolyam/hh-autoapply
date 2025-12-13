import os

class Config:
    chrome_path: str = '/bin/chromium'
    state_path: str = './sessions'
    hh_domain: str = 'hh.ru'
    email: str = 'example@domain.com'
    search_text: str = 'Python Developer'
    model_name: str = ''
    api_key: list = []
    openai_base_url: str = ''
    retries: int = 10
    filter_phrase: str = 'Accept job offers related to Python development.'
    letter_input: str = 'Hello, I am ready to apply for your job!'
    ntfy_url: str = 'https://ntfy.sh'
    ntfy_topic: str = 'ergolyam'
    db_path: str = 'data.db'

    @classmethod
    def load_from_env(cls):
        for key in cls.__annotations__:
            env_value = os.getenv(key.upper())
            if env_value is not None:
                current_value = getattr(cls, key)
                if isinstance(current_value, int):
                    setattr(cls, key, int(env_value))
                elif isinstance(current_value, float):
                    setattr(cls, key, float(env_value))
                elif isinstance(current_value, list):
                    setattr(cls, key, env_value.split(','))
                else:
                    setattr(cls, key, env_value)

Config.load_from_env()

if __name__ == '__main__':
    raise RuntimeError('This module should be run only via main.py')
