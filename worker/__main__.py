import os, sys, asyncio
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from worker.config.config import Config
from worker.core.helpers import Common

from worker.api.get_resume import get_my_resumes

async def main():
    argv = sys.argv[1:]
    resumes = await get_my_resumes()
    resumes_dict = {}
    for idx, r in enumerate(resumes.get("resumes"), start=1):
        resumes_dict[idx] = {
            "resume_id": r.get("id", ""),
            "title": r.get("title", "")
        }
    if not argv:
        print(resumes_dict)
        return
    try:
        idx = int(argv[1])
    except ValueError:
        print(f"The index must be a number, not '{argv[1]}'")
        return
    if len(argv) == 2 and argv[0] == "--set":
        value = resumes_dict.get(idx)
        assert value
        value_id = value.get('resume_id')
        Common.cfg['settings']['resume_id'] = value_id
        Common.cfg.save()
        print(f"Set resume id: {value_id}")

if __name__ == '__main__':
    asyncio.run(main())
