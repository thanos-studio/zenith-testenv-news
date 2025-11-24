FROM python:3.11-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    APP_HOME=/app \
    DJANGO_SETTINGS_MODULE=News.settings \
    DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1 \
    POSTGRES_DB=zenith_news \
    POSTGRES_USER=postgres \
    POSTGRES_PASSWORD=postgres \
    POSTGRES_HOST=db \
    POSTGRES_PORT=5432 \
    PORT=8000

WORKDIR ${APP_HOME}

RUN apt-get update \
    && apt-get install --no-install-recommends -y build-essential libpq-dev libjpeg62-turbo-dev zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

COPY News/requirements.txt ./requirements.txt

RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt gunicorn

COPY News ${APP_HOME}

RUN python manage.py collectstatic --noinput

EXPOSE ${PORT}

CMD ["sh", "-c", "gunicorn News.wsgi:application --bind 0.0.0.0:${PORT}"]
