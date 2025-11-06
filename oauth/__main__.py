import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from oauth.config.config import Config
from oauth.config import logging_config
logging = logging_config.setup_logging(__name__)

logging.info(f'Script initialization, logging level: {Config.log_level}')

def main():
    from oauth.core.api import run_server
    run_server()

if __name__ == '__main__':
    main()
