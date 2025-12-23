import httpx, io, asyncio, time, itertools

import pydantic_ai.models.openai
import pydantic_ai.providers.openai
import pydantic_ai.models.gemini
import pydantic_ai.models.google
import pydantic_ai.providers.google
import pydantic_ai.models.openrouter
import pydantic_ai.providers.openrouter
import pydantic_ai.models.groq
import pydantic_ai.providers.groq
import pydantic_ai.models.cerebras
import pydantic_ai.providers.cerebras

from worker.core.logs import Log


async def take_screenshot(page, *, full_page: bool = False, img_type: str = 'png') -> io.BytesIO:
    data: bytes = await page.screenshot(full_page=full_page, type=img_type)
    return io.BytesIO(data)


class AsyncTimer:
    def __init__(self, delay: float):
        self.delay = delay
        self._last_time = 0.0
        self._lock = asyncio.Lock()

    async def __aenter__(self):
        async with self._lock:
            now = time.monotonic()
            wait = self.delay - (now - self._last_time)
            if wait > 0:
                Log.log.info(f'Sleep {wait}...')
                await asyncio.sleep(wait)

    async def __aexit__(self, exc_type, exc, tb):
        self._last_time = time.monotonic()


class Common():
    client_timeout = httpx.Timeout(30.0)
    http = httpx.AsyncClient(timeout=client_timeout)
    model: pydantic_ai.models.Model
    agent: pydantic_ai.Agent
    openai_model = pydantic_ai.models.openai.OpenAIChatModel
    openai_provider = pydantic_ai.providers.openai.OpenAIProvider
    gemini_model = pydantic_ai.models.google.GoogleModel
    gemini_model_settings = pydantic_ai.models.gemini.GeminiModelSettings
    gemini_model_safety_settings = pydantic_ai.models.gemini.GeminiSafetySettings
    gemini_provider = pydantic_ai.providers.google.GoogleProvider
    openrouter_model = pydantic_ai.models.openrouter.OpenRouterModel
    openrouter_provider = pydantic_ai.providers.openrouter.OpenRouterProvider
    groq_model = pydantic_ai.models.groq.GroqModel
    groq_provider = pydantic_ai.providers.groq.GroqProvider
    cerebras_model = pydantic_ai.models.cerebras.CerebrasModel
    cerebras_provider = pydantic_ai.providers.cerebras.CerebrasProvider
    agent_selection = False
    post_timer = AsyncTimer(10)
    api_timer = AsyncTimer(1)


def selection(boolean: bool) -> bool:
    '''
    accept or reject the vacancy
    example reject vacancy:
    selection(bool(False))
    '''
    Common.agent_selection = boolean
    return boolean


class KeyRotator:
    def __init__(self, keys: list[str]):
        self._it = itertools.cycle(keys)
        self._lock = asyncio.Lock()

    async def next_key(self) -> str:
        async with self._lock:
            return next(self._it)


if __name__ == '__main__':
    raise RuntimeError('This module should be run only via main.py')
