from pydantic_ai.messages import (
    ModelRequest,
    SystemPromptPart
)

from worker.core.helpers import Common, Log
from worker.config.config import settings

agent_selection = bool()

def selection(boolean: bool) -> bool:
    '''
    accept or reject the vacancy
    example reject vacancy:
    selection(bool(False))
    '''
    global agent_selection
    agent_selection = boolean
    return boolean


class VacancyBot:
    def __init__(self):
        self.agent_result = ''
        self.filter_phrase = ''
        self.system_prompt = []

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
        global agent_selection
        agent_selection = False
        for attempt in range(1, settings.retries + 1):
            try:
                result = await Common.agent.run(msg, message_history=self.system_prompt)
                self.agent_result = result.output
                return
            except:
                Log.log.warning(f'An error occurred during attempt {attempt}.')
                if attempt == settings.retries:
                    raise

    def show_selection(self) -> bool:
        return agent_selection

    def show_agent_result(self) -> str:
        Log.agent_panel(
            selection=agent_selection,
            text=self.agent_result
        )
        return self.agent_result


if __name__ == '__main__':
    raise RuntimeError('This module should be run only via main.py')

