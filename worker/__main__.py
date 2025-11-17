import os, sys, asyncio
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from worker.core.helpers import Common

from worker.api.get_resume import resume_request
from worker.api.get_handbook import handbook_request
from worker.funcs.vacancies import cycle_responses
from worker.core.llm import init_llm

async def main():
    argv = sys.argv[1:]
    match argv:
        case ['--help', topic]:
            print(await handbook_request(topic))
        case ['--help']:
            print('''Usage:
script.py --resume <index> - display all resumes or set the active resume by index
script.py --help [ experience, employment, schedule ] - display this message or help on the topic
            ''')
        case ['--resume', idx]:
            resumes = await resume_request()
            try:
                idx = int(idx)
            except ValueError:
                print(f'Invalid index: {idx}')
                return
            value = resumes.get(idx)
            if not value:
                print(f'Resume with index {idx} not found')
                return
            assert value
            value_id = value.get('resume_id')
            Common.cfg['settings']['resume_id'] = value_id
            Common.cfg.save()
            print(f'Set resume id: {value_id}')
        case ['--resume']:
            resumes = await resume_request()
            print(resumes)
        case [] | _ if not argv:
            await init_llm()
            await cycle_responses()
        case _:
            print('Unknown command. Use --help')

if __name__ == '__main__':
    asyncio.run(main())
