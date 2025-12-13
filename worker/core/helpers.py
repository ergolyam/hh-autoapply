import httpx, io, asyncio, time
from itertools import cycle

import pydantic_ai.models.openai
import pydantic_ai.providers.openai
import pydantic_ai.models.gemini
import pydantic_ai.models.google
import pydantic_ai.providers.google


async def take_screenshot(page, *, full_page: bool = False, img_type: str = "png") -> io.BytesIO:
    data: bytes = await page.screenshot(full_page=full_page, type=img_type)
    return io.BytesIO(data)


class Common():
    client_timeout = httpx.Timeout(30.0)
    http = httpx.AsyncClient(timeout=client_timeout)
    client_agent = httpx.AsyncClient(timeout=client_timeout)
    model: pydantic_ai.models.Model
    agent: pydantic_ai.Agent
    openai_model = pydantic_ai.models.openai.OpenAIModel
    openai_provider = pydantic_ai.providers.openai.OpenAIProvider
    gemini_model = pydantic_ai.models.google.GoogleModel
    gemini_model_settings = pydantic_ai.models.gemini.GeminiModelSettings
    gemini_model_safety_settings = pydantic_ai.models.gemini.GeminiSafetySettings
    gemini_provider = pydantic_ai.providers.google.GoogleProvider


class RotatingGeminiKeyClient(httpx.AsyncClient):
    def __init__(self, keys, min_interval: float | None = None, **kwargs):
        kwargs.setdefault('timeout', Common.client_timeout)
        hooks = kwargs.setdefault('event_hooks', {})
        hooks.setdefault('request', []).append(self._before_request)
        self._keys = cycle(keys)
        self._min_interval = min_interval
        self._last_request_ts = 0.0
        self._lock = asyncio.Lock()
        super().__init__(**kwargs)
    async def _before_request(self, request: httpx.Request):
        if self._min_interval is not None:
            async with self._lock:
                now = time.monotonic()
                delta = now - self._last_request_ts
                wait_for = self._min_interval - delta
                if wait_for > 0:
                    await asyncio.sleep(wait_for)
                    now = time.monotonic()
                self._last_request_ts = now
        key = next(self._keys)
        print(f'Use Gemini api key: ...{key[-4:]}')
        request.headers['X-Goog-Api-Key'] = key


class RotatingOpenAIKeyClient(httpx.AsyncClient):
    def __init__(self, keys, **kwargs):
        kwargs.setdefault('timeout', Common.client_timeout)
        hooks = kwargs.setdefault('event_hooks', {})
        hooks.setdefault('request', []).append(self._add_header)
        self._keys = cycle(keys)
        super().__init__(**kwargs)
    async def _add_header(self, request: httpx.Request):
        key = next(self._keys)
        print(f'Use OpenAI api key: ...{key[-4:]}')
        request.headers.pop('Authorization', None)
        request.headers['Authorization'] = f'Bearer {key}'


if __name__ == '__main__':
    raise RuntimeError('This module should be run only via main.py')
