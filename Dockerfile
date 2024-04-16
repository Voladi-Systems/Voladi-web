FROM python:3.10.5-slim-buster as base-stage

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION=1.1.12 \
    POETRY_HOME="/opt/poetry" \
    POETRY_SETTINGS_VIRTUALENVS_CREATE=0 \
    POETRY_NO_INTERACTION=1

RUN apt-get update \
 && apt-get install --no-install-recommends -y \
    gnupg \
    wget \
 && echo "deb http://apt.postgresql.org/pub/repos/apt buster-pgdg main" > /etc/apt/sources.list.d/pgdg.list \
 && wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add - 2>&1

RUN apt-get update \
 && apt-get install --no-install-recommends -y \
    build-essential \
    curl \
    gettext \
    libpcre3 \
    libpcre3-dev \
    nginx \
    wget \
    postgresql-client-15 \
    cron \
 && curl -sL https://deb.nodesource.com/setup_16.x -o /tmp/nodesource_setup.sh \
 && bash /tmp/nodesource_setup.sh \
 && apt-get install -y nodejs \
 && ln -s /usr/bin/node /usr/local/bin/node \
 && ln -s /usr/bin/npm /usr/local/bin/npm \
 && rm -rf /var/lib/apt/lists/*

ENV WAIT_FOR_IT_VERSION 81b1373

RUN wget -O /usr/local/bin/wait-for-it \
    https://raw.githubusercontent.com/vishnubob/wait-for-it/$WAIT_FOR_IT_VERSION/wait-for-it.sh \
 && chmod +x /usr/local/bin/wait-for-it

ENV GOSU_VERSION 1.14

RUN wget -O /usr/local/bin/gosu \
    https://github.com/tianon/gosu/releases/download/$GOSU_VERSION/gosu-amd64 \
 && chmod +x /usr/local/bin/gosu

ENV CONFD_VERSION 0.16.0

RUN wget -O /usr/local/bin/confd \
    https://github.com/kelseyhightower/confd/releases/download/v$CONFD_VERSION/confd-$CONFD_VERSION-linux-amd64 \
 && chmod +x /usr/local/bin/confd

COPY bin/forego /usr/local/bin/forego

RUN chmod +x /usr/local/bin/forego

ENV WORKDIR /app

RUN pip install --upgrade pip \
 && pip install poetry

WORKDIR $WORKDIR

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false \
 && poetry install

RUN mkdir /etc/uwsgi \
 && mkdir /run/uwsgi \
 && mkdir /run/asgi \
 && mkdir /run/nginx \
 && chown www-data:www-data /run/uwsgi \
 && chown -R www-data:www-data /run/nginx/

COPY --chown=www-data:www-data docker-entrypoint.sh /

RUN chmod +x /docker-entrypoint.sh

COPY --chown=www-data:www-data . .

RUN DJANGO_SECRET_KEY=nothing python manage.py tailwind install

ENTRYPOINT ["/docker-entrypoint.sh"]

CMD ["start"]

# TW build stage
FROM base-stage as build-stage

RUN DJANGO_SECRET_KEY=nothing python manage.py povulo build:clean \
 && DJANGO_SECRET_KEY=nothing python manage.py povulo build:tailwind
