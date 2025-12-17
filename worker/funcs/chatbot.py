from pydantic_ai.messages import (
    ModelRequest,
    SystemPromptPart
)

from worker.core.llm import build_model_for_key

from worker.core.helpers import Common, Log, KeyRotator
from worker.config.config import settings


class VacancyBot:
    def __init__(self):
        self.agent_result = ''
        self.filter_phrase = ''
        self.system_prompt = []
        self.key_rotator = KeyRotator(settings.api_keys)

    def set_filter_phrase(self, phrase):
        self.filter_phrase = phrase
        self.system_prompt = [
            ModelRequest(
                parts=[
                    SystemPromptPart(content=self.filter_phrase)
                ]
            )
        ]

    async def run_bot(self, msg: str):
        Common.agent_selection = False
        for attempt in range(1, settings.retries + 1):
            model_kwargs = {}
            if len(settings.api_keys) > 1:
                api_key = await self.key_rotator.next_key()
                Log.log.info(f'Use api key: {api_key[-4:]}')
                model = build_model_for_key(api_key)
                model_kwargs['model'] = model
            try:
                result = await Common.agent.run(
                    msg,
                    message_history=self.system_prompt,
                    **model_kwargs
                )
                self.agent_result = result.output
                return
            except Exception as e:
                Log.log.warning(f'An error occurred during attempt {attempt}.\n{e}')
                if attempt == settings.retries:
                    raise

    def show_selection(self) -> bool:
        return Common.agent_selection

    def show_agent_result(self) -> str:
        Log.agent_panel(
            selection=Common.agent_selection,
            text=self.agent_result
        )
        return self.agent_result


if __name__ == '__main__':
    raise RuntimeError('This module should be run only via main.py')

