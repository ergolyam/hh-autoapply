from aiohttp import web, ClientSession
from oauth.config.config import Config

client_id = Config.hhapp_id
client_secret = Config.hhapp_secret
redirect_uri = Config.redirect_uri

async def authorize(request):
    auth_url = (
        f"https://hh.ru/oauth/authorize?"
        f"response_type=code&client_id={client_id}&redirect_uri={redirect_uri}"
    )
    raise web.HTTPFound(auth_url)

async def callback(request):
    code = request.query.get("code")
    if not code:
        return web.Response(text="Error: authorization code is not received", status=400)
    
    token_url = "https://hh.ru/oauth/token"
    data = {
        "grant_type": "authorization_code",
        "code": code,
        "client_id": client_id,
        "client_secret": client_secret,
        "redirect_uri": redirect_uri,
    }
    
    async with ClientSession() as session:
        async with session.post(token_url, data=data) as resp:
            if resp.status == 200:
                token_response = await resp.json()
                access_token = token_response.get("access_token")
                return web.Response(text=f"Access token: {access_token}")
            else:
                error = await resp.json()
                return web.Response(text=f"Error: {error}", status=resp.status)

async def redirect_root(request):
    raise web.HTTPFound('/login')

def run_server():
    app = web.Application()
    app.add_routes([
        web.get('/', redirect_root),
        web.get('/login', authorize),
        web.get('/' + '/'.join(redirect_uri.split('/')[3:]), callback)
    ])

    web.run_app(app, host=Config.api_host, port=Config.api_port)

if __name__ == "__main__":
    raise RuntimeError("This module should be run only via main.py")
