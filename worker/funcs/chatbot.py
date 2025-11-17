from worker.core.helpers import Common
from pydantic_ai.messages import (
    ModelRequest,
    SystemPromptPart
)

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
        result = await Common.agent.run(msg, message_history=self.system_prompt)
        self.agent_result = result.output

    def show_selection(self) -> bool:
        print(f'Selection call: {agent_selection}')
        return agent_selection

    def show_agent_result(self) -> str:
        print(f'Agent result: {self.agent_result}')
        return self.agent_result


if __name__ == '__main__':
    raise RuntimeError('This module should be run only via main.py')

