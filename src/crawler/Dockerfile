FROM python:3.11-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

COPY src/crawler /app/crawler
COPY src/database /app/database
COPY ./project.toml /app/
COPY ./uv.lock /app/

WORKDIR /app
RUN uv sync --frozen --no-cache --extra crawler

ENV PYTHONPATH="${PYTHONPATH}:/app/database" 

CMD ["python","crawler/main.py"]
