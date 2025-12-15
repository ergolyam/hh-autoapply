from worker.config.config import settings
from tortoise import Tortoise


async def init():
    await Tortoise.init(
        db_url=f'sqlite://{settings.db_path}',
        modules={'models': ['worker.db.models']}
    )
    await Tortoise.generate_schemas()

    
async def close():
    await Tortoise.close_connections()


if __name__ == '__main__':
    raise RuntimeError('This module should be run only via main.py')
