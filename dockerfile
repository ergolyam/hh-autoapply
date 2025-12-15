FROM ghcr.io/astral-sh/uv:python3.12-trixie-slim AS builder

WORKDIR /app

COPY pyproject.toml uv.lock /app

RUN uv sync --no-cache


FROM python:3.12-slim-trixie AS main

RUN apt-get update -y

RUN apt-get install -y --no-install-recommends chromium

RUN rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY --from=builder /app/.venv /app/.venv

COPY . /app

ENV PATH="/app/.venv/bin:$PATH"

ENV PYTHONDONTWRITEBYTECODE=1

ENV PYTHONUNBUFFERED=1

ENV CHROME_PATH="/usr/bin/chromium"

ENV DATA_PATH="/app/data/"

CMD ["python", "worker"]

