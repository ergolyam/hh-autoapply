from worker.core.helpers import Common
from worker.config.config import Config

async def request(path: str):
    headers = {
        "Authorization": f"Bearer {Common.cfg['settings']['oauth_token']}",
        "User-Agent": f"{Config.app_name}/1.0 ({Config.app_email})",
    }
    
    url = f"https://{Config.hh_api_domain}/{path}"
    
    response = await Common.http.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        return {"ok": True, "data": data}

    try:
        err = response.json()
        details = err.get("description") or err.get("error") or err
    except Exception:
        details = response.text
    return {"ok": False, "status_code": response.status_code, "details": details}

if __name__ == "__main__":
    raise RuntimeError("This module should be run only via main.py")
