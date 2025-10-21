FROM ghcr.io/astral-sh/uv:python3.12-alpine AS builder

ARG EXTRA

WORKDIR /app

COPY pyproject.toml uv.lock /app

RUN uv sync --no-cache --extra ${EXTRA}


FROM python:3.12-alpine AS main

ARG EXTRA

WORKDIR /app

COPY --from=builder /app/.venv /app/.venv

COPY ./${EXTRA} /app/${EXTRA}

RUN echo -e "#!/usr/bin/env sh\npython ${EXTRA}" | tee ./start.sh

RUN chmod +x ./start.sh

ENV PATH="/app/.venv/bin:$PATH"

ENV PYTHONDONTWRITEBYTECODE=1

ENV PYTHONUNBUFFERED=1

CMD ["./start.sh"]

