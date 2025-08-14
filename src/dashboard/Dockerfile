FROM python:3.11-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

COPY ./src/dashboard /app/dashboard
COPY ./src/database /app/database
COPY ./pyproject.toml /app/
COPY ./uv.lock /app/
COPY ./src/dashboard/main.py /app/

WORKDIR /app
RUN uv sync --frozen --no-cache --extra dashboard

ENV STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

CMD ["/app/.venv/bin/streamlit","run","/app/main.py"]
