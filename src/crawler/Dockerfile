FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && \
    apt-get install -y gcc libpq-dev python3-dev && \
    rm -rf /var/lib/apt/lists/*

COPY src/crawler/requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

ENV PYTHONPATH="${PYTHONPATH}:/app/database"

COPY src/crawler /app/crawler
COPY src/database /app/database 

CMD ["prefect","server","start","&&","python","crawler/main.py"]
