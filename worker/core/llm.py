import pydantic_ai
from typing import Any, Literal

from worker.config.config import settings
from worker.core.helpers import Common, selection

provider, model_name = settings.model_name.split(':', 1)
model_cache = {}

def build_model_for_key(api_key: str):
    if api_key in model_cache:
        return model_cache[api_key]
    match provider:
        case 'google' | 'gemini':
            model = Common.gemini_model(
                model_name=model_name,
                provider=Common.gemini_provider(api_key=api_key),
            )
        case 'openai':
            model = Common.openai_model(
                model_name=model_name,
                provider=Common.openai_provider(
                    api_key=api_key,
                    base_url=settings.openai_base_url,
                ),
            )
        case 'openrouter':
            model = Common.openrouter_model(
                model_name=model_name,
                provider=Common.openrouter_provider(api_key=api_key),
            )
        case 'groq':
            model = Common.groq_model(
                model_name=model_name,
                provider=Common.groq_provider(api_key=api_key),
            )
        case 'cerebras':
            model = Common.cerebras_model(
                model_name=model_name,
                provider=Common.cerebras_provider(api_key=api_key),
            )
        case _:
            raise ValueError(f'Unknown provider: {provider}')
    model_cache[api_key] = model
    return model


async def init_llm():
    agent_kwargs: dict[str, Any] = {}
    Common.model = build_model_for_key(settings.api_keys[0])
    if provider in ('google', 'gemini'):
        categories = (
            'HARM_CATEGORY_SEXUALLY_EXPLICIT',
            'HARM_CATEGORY_HATE_SPEECH',
            'HARM_CATEGORY_HARASSMENT',
            'HARM_CATEGORY_DANGEROUS_CONTENT',
            'HARM_CATEGORY_CIVIC_INTEGRITY',
        )
        agent_kwargs['model_settings'] = Common.gemini_model_settings(
            gemini_safety_settings=[
                Common.gemini_model_safety_settings(
                    category=cat,
                    threshold='BLOCK_NONE',
                )
                for cat in categories
            ]
        )
    Common.agent = pydantic_ai.Agent(
        Common.model,
        tools=[
            pydantic_ai.Tool(selection),
        ],
        **agent_kwargs
    )


if __name__ == '__main__':
    raise RuntimeError('This module should be run only via main.py')

