FROM python:3.11.5-slim-bullseye as builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY ./requirements.txt .

RUN pip install --no-cache-dir --upgrade pip && \
    pip wheel --no-cache-dir --no-deps --wheel-dir=/app/wheels -r ./requirements.txt


FROM python:3.11.5-slim-bullseye

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY --from=builder /app/wheels /wheels

RUN pip install --no-cache-dir /wheels/*

COPY ./src/alembic.ini ./alembic.ini
COPY ./src/migrations ./migrations
COPY ./src/core ./core
COPY ./src/database ./database

CMD ["alembic", "upgrade", "head"]
