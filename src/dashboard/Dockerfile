FROM python:3.11-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

COPY ./src/dashboard /app/dashboard
COPY ./src/database /app/database
COPY ./project.toml /app/
COPY ./uv.lock /app/

WORKDIR /app
RUN uv sync --frozen --no-cache --extra dashboard

ENV PYTHONPATH="${PYTHONPATH}:/app/database"

ENV STREAMLIT_BROWSER_GATHER_USAGE_STATS=false


CMD ["streamlit", "run","dashboard/main.py"]
