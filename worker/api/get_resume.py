from worker.core.helpers import Common
from worker.config.config import Config
from worker.config import logging_config
logging = logging_config.setup_logging(__name__)

async def get_my_resumes():
    headers = {
        "Authorization": f"Bearer {Common.cfg['settings']['oauth_token']}",
        "User-Agent": f"{Config.app_name}/1.0 ({Config.app_email})",
    }
    
    url = f"https://{Config.hh_api_domain}/resumes/mine"
    
    response = await Common.http.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        resumes = data.get("items", [])
        
        info = "Your resumes:\n"
        for r in resumes:
            resume_id = r.get("id", "")
            title = r.get("title", "")
            status = r.get("status", {}).get("id", "")
            
            info += f"- ID: {resume_id}, Title: {title}, Status: {status}\n"
        
        if not resumes:
            info += "(empty)\n"
        return info
    else:
        try:
            err = response.json()
            details = err.get("description") or err.get("error") or err
        except Exception:
            details = response.text
        return f"Error receiving CV. Code: {response.status_code}, Text: {details}"

if __name__ == "__main__":
    raise RuntimeError("This module should be run only via main.py")
