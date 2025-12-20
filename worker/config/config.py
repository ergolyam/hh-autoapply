from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    data_path: str = './data'
    chrome_path: str = '/bin/chrome'
    hh_domain: str = 'hh.ru'
    email: str
    model_name: str
    api_keys: list
    openai_base_url: str = ''
    retries: int = 10
    search_text: str
    filter_phrase: str
    letter_input: str
    employer_block: list = []
    ntfy_url: str = 'https://ntfy.sh'
    ntfy_topic: str

    class Config:
        env_file = ".env"
        
settings = Settings() # type: ignore[call-arg]

if __name__ == '__main__':
    raise RuntimeError('This module should be run only via main.py')
