import httpx, io

import pydantic_ai.models.openai
import pydantic_ai.providers.openai
import pydantic_ai.models.gemini
import pydantic_ai.models.google
import pydantic_ai.providers.google
import pydantic_ai.models.openrouter
import pydantic_ai.providers.openrouter


async def take_screenshot(page, *, full_page: bool = False, img_type: str = "png") -> io.BytesIO:
    data: bytes = await page.screenshot(full_page=full_page, type=img_type)
    return io.BytesIO(data)


class Common():
    client_timeout = httpx.Timeout(30.0)
    http = httpx.AsyncClient(timeout=client_timeout)
    client_agent = httpx.AsyncClient(timeout=client_timeout)
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


if __name__ == '__main__':
    raise RuntimeError('This module should be run only via main.py')
