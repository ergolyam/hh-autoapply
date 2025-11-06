import os, sys, asyncio
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from worker.config.config import Config
from worker.core.helpers import Common

from worker.api.get_resume import resume_request

async def main():
    argv = sys.argv[1:]
    resumes = await resume_request()
    if not argv:
        print(resumes)
        return
    try:
        idx = int(argv[1])
    except ValueError:
        print(f"The index must be a number, not '{argv[1]}'")
        return
    if len(argv) == 2 and argv[0] == "--set":
        value = resumes.get(idx)
        assert value
        value_id = value.get('resume_id')
        Common.cfg['settings']['resume_id'] = value_id
        Common.cfg.save()
        print(f"Set resume id: {value_id}")

if __name__ == '__main__':
    asyncio.run(main())
