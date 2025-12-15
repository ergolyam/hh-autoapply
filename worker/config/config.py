import os
from typing import get_origin, get_args, Union
from types import UnionType

class Config:
    data_path: str = 'data'
    chrome_path: str = '/bin/chrome'
    state_path: str = f'{data_path}/sessions'
    db_path: str = f'{data_path}/data.db'
    hh_domain: str = 'hh.ru'
    email: str | None = None
    model_name: str | None = None
    api_key: str | None = None
    openai_base_url: str = ''
    retries: int = 10
    search_text: str| None = None
    filter_phrase: str | None = None
    letter_input: str | None = None
    ntfy_url: str = 'https://ntfy.sh'
    ntfy_topic: str = 'ergolyam'

    @classmethod
    def load_from_env(cls):
        for key, annotation in cls.__annotations__.items():
            env_value = os.getenv(key.upper())
            if env_value is None:
                continue
            origin = get_origin(annotation)
            args = get_args(annotation)
            if origin in (Union, UnionType) and type(None) in args:
                target_type = next(t for t in args if t is not type(None))
            else:
                target_type = annotation
            if target_type is int:
                value = int(env_value)
            elif target_type is float:
                value = float(env_value)
            elif target_type is bool:
                value = env_value.lower() in ('1', 'true', 'yes')
            elif target_type is list:
                value = env_value.split(',')
            else:
                value = env_value
            setattr(cls, key, value)
        cls._validate_required()

    @classmethod
    def _validate_required(cls):
        missing = [
            key for key in cls.__annotations__
            if getattr(cls, key) is None
        ]
        if missing:
            raise RuntimeError(
                f'Required parameters are not specified: {', '.join(missing)}'
            )

Config.load_from_env()

if __name__ == '__main__':
    raise RuntimeError('This module should be run only via main.py')
