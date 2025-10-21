import os, sys, asyncio
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from worker.config.config import Config
from worker.config.config_yaml import load_config

from worker.config import logging_config
logging = logging_config.setup_logging(__name__)

logging.info(f"Script initialization, logging level: {Config.log_level}")

async def main():
    from worker.api.get_resume import get_my_resumes
    load_config()
    print(await get_my_resumes())

if __name__ == '__main__':
    asyncio.run(main())
