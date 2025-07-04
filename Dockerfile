# ─── build stage ─────────────────────────────────────────────────────────────
FROM python:3.11-slim AS base
WORKDIR /app

# install Poetry
RUN pip install --no-cache-dir poetry

# copy only pyproject.toml & poetry.lock for dependency install
COPY pyproject.toml poetry.lock* /app/

# configure and install *only* the main dependencies (skip the project itself)
RUN poetry config virtualenvs.create false \
 && poetry install --only main --no-interaction --no-ansi --no-root

# ─── copy your source ────────────────────────────────────────────────────────
COPY app /app/app
COPY .env /app/.env

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
