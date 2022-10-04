# base image
FROM python:3.9.5-slim as python-base

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    APP_PATH="/app" \
    VENV_PATH="/app/.venv"

# prepend poetry and venv to path
ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

WORKDIR $APP_PATH


# Build
FROM python-base as builder-base

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

RUN apt-get update \
    && apt-get --no-install-recommends install -y curl=7.64.0-4+deb10u3 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && curl -sSL https://install.python-poetry.org | python

ENV PATH="${PATH}:/root/.local/bin"


COPY pyproject.toml poetry.lock ./

# install deps
RUN poetry install --only main --no-root


# Prod
FROM python-base as production
# copy deps
COPY --from=builder-base $APP_PATH $APP_PATH

# copy code
COPY . $APP_PATH

# install git and make gitflow executable
RUN apt-get update \
    && apt-get --no-install-recommends install -y git=1:2.20.1-2+deb10u3 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && chmod +x /app/scripts/* && cp /app/scripts/* /usr/local/bin

ENTRYPOINT ["python", "main.py"]
