import httpx
from worker.config.config_yaml import YamlConfig

class Common():
    http = httpx.AsyncClient(timeout=30)
    cfg = YamlConfig()
