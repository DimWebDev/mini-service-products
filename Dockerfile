# ─── Build stage ─────────────────────────────────────────────────────────────
FROM python:3.11-slim AS base
WORKDIR /app

# install Poetry
RUN pip install --no-cache-dir poetry

# copy only pyproject.toml & poetry.lock for dependency install
COPY pyproject.toml poetry.lock* /app/

# install ALL dependencies (main + dev) so alembic CLI is available
RUN poetry config virtualenvs.create false \
 && poetry install --no-interaction --no-ansi --no-root

# ─── copy your source + migration config ────────────────────────────────────
COPY app       /app/app
COPY .env      /app/.env
COPY alembic.ini /app/alembic.ini
COPY alembic     /app/alembic

# ─── expose & run: stamp then serve ─────────────────────────────────────────
EXPOSE 8000
CMD ["sh", "-c", "alembic stamp head && uvicorn app.main:app --host 0.0.0.0 --port 8000"]
