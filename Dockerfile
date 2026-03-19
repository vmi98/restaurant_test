FROM python:3.11-slim

RUN apt-get update && apt-get install -y build-essential libpq-dev && rm -rf /var/lib/apt/lists/*

WORKDIR /app

RUN python -m pip install --upgrade pip && pip install uv

COPY pyproject.toml uv.lock ./

RUN uv sync

COPY . .

RUN useradd -m -d /app django && chown -R django:django /app
USER django

EXPOSE 8000

CMD uv run manage.py migrate --settings=config.settings.dev && \
    uv run manage.py load_data --settings=config.settings.dev && \
    uv run manage.py runserver 0.0.0.0:8000 --settings=config.settings.dev