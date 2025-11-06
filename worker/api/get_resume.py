from worker.api.base import request

async def resume_request() -> dict:
    resp = await request('resumes/mine')
    if resp.get('ok', False):
        data = resp.get('data', [])
        items = data.get('items', [])
        resumes_dict = {}
        for idx, r in enumerate(items, start=1):
            resumes_dict[idx] = {
                "resume_id": r.get("id", ""),
                "title": r.get("title", "")
            }
        return resumes_dict
    else:
        raise Exception(f'Error {resp.get('status_code', None)} receiving resume: {resp.get('details', None)}')


if __name__ == "__main__":
    raise RuntimeError("This module should be run only via main.py")
