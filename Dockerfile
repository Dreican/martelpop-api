FROM python:3.14-slim
LABEL authors="Dreican"

RUN apt-get update \
    && apt-get install -y --no-install-recommends postgresql-client \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /code

COPY ./requirements.txt .

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY . .

COPY scripts/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]