import yaml, os

from worker.config.config import Config

config_path = Config.config_path

default_config = {
    "settings": {
        "oauth_token": "abcde12345",
    },
    "filters": {
        "only_with_salary": False,
        "currency": "RUR",
        "professional_role": 1,
        "experience": 1
    }
}


def load_config(path: str = config_path, defaults: dict = {} ) -> dict:
    defaults = defaults or default_config

    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8") as f:
            yaml.safe_dump(defaults, f, allow_unicode=True, sort_keys=False)
        print(f"New configuration created: {path}")

    with open(path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f) or {}

    updated = _merge_defaults(config, defaults)

    if updated:
        with open(path, "w", encoding="utf-8") as f:
            yaml.safe_dump(config, f, allow_unicode=True, sort_keys=False)

    return config


def _merge_defaults(config: dict, defaults: dict) -> bool:
    updated = False
    for key, val in defaults.items():
        if key not in config:
            config[key] = val
            updated = True
        elif isinstance(val, dict):
            if _merge_defaults(config[key], val):
                updated = True
    return updated


class YamlConfig:
    def __init__(self, path=config_path, defaults=None):
        self.path = path
        self.defaults = defaults or default_config
        self.data = load_config(path, self.defaults)

    def save(self):
        with open(self.path, "w", encoding="utf-8") as f:
            yaml.safe_dump(self.data, f, allow_unicode=True, sort_keys=False)

    def __getitem__(self, item):
        return self.data[item]

    def __setitem__(self, key, value):
        self.data[key] = value
        self.save()


if __name__ == "__main__":
    raise RuntimeError("This module should be run only via main.py")
