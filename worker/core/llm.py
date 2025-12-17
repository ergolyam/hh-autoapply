import pydantic_ai
from typing import Any, Literal, cast

from worker.config.config import settings
from worker.core.helpers import Common

from worker.funcs.chatbot import selection


async def init_llm():
    provider, model_name = settings.model_name.split(':', 1)
    agent_kwargs: dict[str, Any] = {}
    match provider:
        case 'google' | 'gemini':
            Common.model = Common.gemini_model(
                model_name=model_name,
                provider=Common.gemini_provider(
                    api_key=settings.api_key
                )
            )
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
                        category=cast(
                            Literal[
                                'HARM_CATEGORY_SEXUALLY_EXPLICIT',
                                'HARM_CATEGORY_HATE_SPEECH',
                                'HARM_CATEGORY_HARASSMENT',
                                'HARM_CATEGORY_DANGEROUS_CONTENT',
                                'HARM_CATEGORY_CIVIC_INTEGRITY',
                            ],
                            cat,
                        ),
                        threshold='BLOCK_NONE',
                    )
                    for cat in categories
                ]
            )
        case 'openai':
            Common.model = Common.openai_model(
                model_name=model_name,
                provider=Common.openai_provider(
                    api_key=settings.api_key,
                    base_url=settings.openai_base_url
                ),
            )
        case 'openrouter':
            Common.model = Common.openrouter_model(
                model_name=model_name,
                provider=Common.openrouter_provider(
                    api_key=settings.api_key,
                )
            )
        case 'groq':
            Common.model = Common.groq_model(
                model_name=model_name,
                provider=Common.groq_provider(
                    api_key=settings.api_key,
                )
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

