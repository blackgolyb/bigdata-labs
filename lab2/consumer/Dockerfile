ARG BASE_IMAGE=python:3.11-slim-buster
FROM $BASE_IMAGE

# system update & package install
RUN apt-get -y update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    postgresql-client \
    openssl libssl-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && pip install poetry \
    && poetry config virtualenvs.in-project true

COPY . .
WORKDIR .

# pip & requirements
RUN poetry install --only main

# RUN adduser app -DHh . -u 1000
# USER 1000

# Execute
CMD ["./.venv/bin/python", "main.py"]
