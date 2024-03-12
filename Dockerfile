FROM python:3.10-slim

ARG name=layout-visualizer
ARG workdir=/workspaces/${name}
WORKDIR ${workdir}

RUN apt-get update && apt-get upgrade -y && \
    apt-get install -y --no-install-recommends python3-dev \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir --upgrade pip==24.0 && \
    pip install --no-cache-dir poetry==1.8.2 && \
    rm -rf /root/.cache/pip

# Install pip dependencies
COPY pyproject.toml poetry.lock ./
ENV POETRY_VIRTUALENVS_CREATE=false
RUN poetry install --no-root --no-interaction --only main
COPY . ./
RUN poetry install --only main --no-interaction
