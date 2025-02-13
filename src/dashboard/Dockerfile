FROM python:3.11-slim

WORKDIR /app

RUN apt-get update --no-cache && \
    apt-get install -y gcc libpq-dev python3-dev && \
    rm -rf /var/lib/apt/lists/*

COPY src/dashboard/requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

ENV PYTHONPATH="${PYTHONPATH}:/app/database"

ENV STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

COPY src/dashboard /app/dashboard
COPY src/database /app/database

CMD ["streamlit", "run","dashboard/main.py"]
