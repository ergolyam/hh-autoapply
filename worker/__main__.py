import os, sys, asyncio
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from worker.config.config import Config
from worker.config.config_yaml import load_config

from worker.api.get_resume import get_my_resumes

async def main():
    resumes = await get_my_resumes()
    resumes_dict = {}
    for idx, r in enumerate(resumes.get("resumes"), start=1):
        resumes_dict[idx] = {
            "resume_id": r.get("id", ""),
            "title": r.get("title", "")
        }
    print(resumes_dict)

if __name__ == '__main__':
    asyncio.run(main())
