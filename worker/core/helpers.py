import httpx, io, logging
from contextvars import ContextVar
from contextlib import contextmanager

import pydantic_ai.models.openai
import pydantic_ai.providers.openai
import pydantic_ai.models.gemini
import pydantic_ai.models.google
import pydantic_ai.providers.google
import pydantic_ai.models.openrouter
import pydantic_ai.providers.openrouter

from rich.console import Console
from rich.panel import Panel
from rich.logging import RichHandler
from rich.markdown import Markdown
from rich.align import Align

async def take_screenshot(page, *, full_page: bool = False, img_type: str = 'png') -> io.BytesIO:
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


_vacancy_id_var: ContextVar[str] = ContextVar('vacancy_id', default='')

class _VacancyContextFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        vid = _vacancy_id_var.get()
        record.vacancy_id = vid
        record.vacancy_prefix = f'[{vid}] ' if vid else ''
        return True


class Log():
    console = Console()
    logging.basicConfig(
        level='INFO',
        format='%(message)s',
        datefmt='[%X]',
        handlers=[RichHandler(rich_tracebacks=True)]
    )
    log = logging.getLogger('rich')
    log.setLevel(logging.INFO)
    log.propagate = False

    _handler = RichHandler(rich_tracebacks=True)
    _handler.addFilter(_VacancyContextFilter())
    _handler.setFormatter(logging.Formatter('%(vacancy_prefix)s%(message)s', datefmt='[%X]'))

    if not log.handlers:
        log.addHandler(_handler)

    logging.getLogger('httpx').setLevel(logging.WARNING)

    @classmethod
    @contextmanager
    def vacancy(cls, vid: str, *, rule: bool = True):
        token = _vacancy_id_var.set(str(vid))
        try:
            if rule:
                cls.console.rule(f'[bold cyan]Vacancy {vid}[/bold cyan]')
            yield
        finally:
            _vacancy_id_var.reset(token)

    @classmethod
    def agent_panel(cls, selection: bool, text: str):
        content = Markdown(text) if isinstance(text, str) else text

        panel = Panel(
            Align.left(content),
            title=f'agent_selection = {selection}',
            border_style='bright_magenta' if selection else 'red',
            padding=(1, 2),
            width=90,
        )

        cls.console.print(panel)


if __name__ == '__main__':
    raise RuntimeError('This module should be run only via main.py')
