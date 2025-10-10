import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from worker.config.config import Config
from worker.config.config_yaml import load_config, YamlConfig

from worker.config import logging_config
logging = logging_config.setup_logging(__name__)

logging.info(f"Script initialization, logging level: {Config.log_level}")

def main():
    config = load_config()
    cfg = YamlConfig()
    logging.debug(cfg['settings']['oauth_token'])

if __name__ == '__main__':
    main()
