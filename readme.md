# hh-autoapply
This project is an auto-apply helper for HeadHunter (hh.ru) that uses Playwright to browse vacancies, an LLM to decide whether to respond, and ntfy to send notifications (including screenshots). It stores processed vacancies in SQLite to avoid duplicate responses.

### Initial Setup

1. **Clone the repository**: Clone this repository using `git clone`.
2. **Create Virtual Env**: Create a Python Virtual Environment `venv` to download the required dependencies and libraries.
3. **Download Dependencies**: Download the required dependencies into the Virtual Environment `venv` using `uv`.
4. **Install a Chrome/Chromium binary**: Ensure Chrome/Chromium exists and set `CHROME_PATH` if needed (default: `/bin/chrome`).

```shell
git clone https://github.com/ergolyam/hh-autoapply.git
cd hh-autoapply
python -m venv .venv
.venv/bin/python -m pip install uv
.venv/bin/python -m uv sync
````

## Usage

### Deploy

- Recommended: create a `.env` file (the app reads env vars from `.env`):
    ```dotenv
    # Required
    EMAIL="you@example.com"
    MODEL_NAME="openai:gpt-4o-mini"   # provider:model (see MODEL_NAME notes below)
    API_KEYS="['key1', 'key2']"
    SEARCH_TEXT="python developer"
    FILTER_PHRASE="System prompt / rules for selecting vacancies"
    LETTER_INPUT="Your cover letter text"
    NTFY_TOPIC="your_ntfy_topic"

    # Optional
    HH_DOMAIN="hh.ru"
    NTFY_URL="https://ntfy.sh"
    NTFY_SUFFIX="False"
    OPENAI_BASE_URL=""
    RETRIES=10
    DATA_PATH="data"
    CHROME_PATH="/bin/chrome"
    EMPLOYER_BLOCK="['id1', 'id2']"
    ```

- Run:
    ```bash
    .venv/bin/python worker
    ```
    - it may ask for captcha text and the email OTP code; then it saves a Playwright session state under `STATE_PATH/<email>.json` for future runs. 

## Environment Variables

The following environment variables control the startup of the project:

| Variable          | Values                                                      | Description                                                           |
| ----------------- | ----------------------------------------------------------- | --------------------------------------------------------------------- |
| `EMAIL`           | *string*                                                    | Login email for hh.ru (used for auth and session state file naming).  |
| `HH_DOMAIN`       | *string*                                                    | HeadHunter domain (default `hh.ru`).                                  |
| `SEARCH_TEXT`     | *string*                                                    | Vacancy search query used on `/search/vacancy`.                       |
| `FILTER_PHRASE`   | *string*                                                    | System prompt / filtering rules for the LLM agent.                    |
| `LETTER_INPUT`    | *string*                                                    | Text inserted into the response letter when applying.                 |
| `MODEL_NAME`      | *string* (`openai:...`, `gemini:...`, `openrouter:...`, `groq:...`, `cerebras:...`) | LLM provider + model in `provider:model` format.                      |
| `EMPLOYER_BLOCK`  | *list* (`"['id1', 'id2']"`)                                 | Filter vacancies by employer id                                       |
| `API_KEYS`        | *list* (`"['key1', 'key2']"`)                               | API keys for the selected LLM provider.                               |
| `OPENAI_BASE_URL` | *string*                                                    | Optional OpenAI-compatible base URL (default empty).                  |
| `RETRIES`         | *integer*                                                   | Number of retries for LLM calls (default `10`).                       |
| `DATA_PATH`       | *string*                                                    | Base data directory (default `data`).                                 |
| `CHROME_PATH`     | *string*                                                    | Path to Chrome/Chromium executable (default `/bin/chrome`).           |
| `NTFY_URL`        | *URL*                                                       | ntfy base URL (default `https://ntfy.sh`).                            |
| `NTFY_TOPIC`      | *string*                                                    | ntfy topic name used for notifications.                               |
| `NTFY_SUFFIX`     | *bool*                                                      | ntfy subtopics available `true`, `false`, `access`, `error`           |

## Features

- **Vacancy Search & Scraping**: Iterates vacancy search pages, opens each vacancy, and extracts key fields (title, schedule, salary, description, skills). 
- **LLM-Based Decision**: Sends vacancy info to an agent that returns a decision (apply / skip) plus commentary. 
- **Auto-Response**: If selected, submits a response letter to the vacancy (when allowed by the UI). 
- **SQLite Deduplication**: Stores processed vacancies (and whether you applied) to prevent repeats. 
- **ntfy Notifications**: Sends messages and screenshots for visibility and error reporting. 
