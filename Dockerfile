# base image
FROM python:3.9.5

SHELL ["/bin/bash", "-o", "pipefail", "-c"]
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
ENV PATH="${PATH}:/root/.poetry/bin"

WORKDIR /app

COPY pyproject.toml poetry.lock ./
RUN poetry config virtualenvs.create false && \
    poetry install --no-dev --no-root

COPY . /app/

RUN echo 'alias gitflow="python /app/main.py"' >> ~/.bashrc

ENTRYPOINT ["python", "main.py"]
