# Prologue
This repository contains a minimal product-management microservice. It’s built with FastAPI for the HTTP API, SQLModel (Pydantic + SQLAlchemy) for ORM models, Postgres for persistent storage, and Alembic for versioned schema migrations. Everything runs in Docker Compose—so you get a single docker compose up --build command that builds the API image, launches Postgres, applies any database migrations, and serves your CRUD endpoints on port 8000.

## 1. Running the App via Docker Compose

This “container-only” workflow builds both the API and the Postgres database, applies any Alembic migrations (if you’ve wired them into your Dockerfile), and then serves the FastAPI app on port 8000.

```bash
docker compose up --build
```

* **Purpose**:

    1. **Build** the Docker images (`api` + `db`).
    2. **Start** the Postgres service and wait for its healthcheck.
    3. **Launch** the API container, which (via your `CMD`) runs `alembic stamp/upgrade head` or `metadata.create_all()` and then starts Uvicorn.

Once you see:

```
api_1  | INFO:     Uvicorn running on http://0.0.0.0:8000
```

you know the service is up.

### Exercising the Endpoints

```bash
curl -X POST http://localhost:8000/products \
     -H "Content-Type: application/json" \
     -d '{"name":"Widget","price":19.99}'

curl http://localhost:8000/products
```

* **Purpose**:

    * The first `curl` creates a product.
    * The second retrieves the list of products.

---

## 2. Git Setup

Initialize your repository and ensure you never commit sensitive credentials.

```bash
git init
```

* **Purpose**: Create a new Git repository in your project folder.

```bash
echo ".env" >> .gitignore
```

* **Purpose**: Prevent your `.env` (which contains `DATABASE_URL`) from being committed.

```bash
git add .
git commit -m "Initial commit: containerized FastAPI + Postgres scaffold"
```

* **Purpose**: Stage all files and record the baseline state of your project.

---

## 3. (Optional) Local “Poetry” Invocation

If you ever want to run the app on your **host** machine instead of inside Docker—for rapid iteration or debugging—you can point at a local Postgres instance.

1. **Start only the database** in Docker:

   ```bash
   docker compose up -d db
   ```

    * **Purpose**: Bring up Postgres without the API container.

2. **Create a `.env.local`** file alongside your `.env`:

   ```
   DATABASE_URL=postgresql+psycopg2://postgres:postgres@localhost:5432/products
   ```

    * **Purpose**: Override the `db:5432` hostname with `localhost:5432`.

3. **Launch the app with Poetry**:

   ```bash
   poetry run dotenv run --file .env.local -- uvicorn app.main:app --reload
   ```

    * **Purpose**:

        1. Loads `DATABASE_URL` from `.env.local`.
        2. Starts Uvicorn in “reload” mode for live code changes.

> **Note**: If “container only” is your goal you can safely skip this entire section.

---

## 4. Database Migrations (Alembic)

> **Clarification**: “Migrations” here refers **only** to **schema changes** within your database (adding/removing tables or columns), *not* to moving between different database engines.

### 4.1 When to Run Migrations

Any time you change your SQLModel classes in `app/models.py` (e.g. add a new field, change a type), you must:

1. **Generate** a new migration script.
2. **Apply** that script to your database.

This gives you full control over exactly when and how your schema evolves.

---

### 4.2 Manual Migration Workflow

1. **Edit your model**
   e.g. in `app/models.py` add:

   ```python
   neues_feld: int | None = Field(default=None, description="Beispiel-Feld")
   ```

2. **Generate a migration**

   ```bash
   docker compose run --rm -v "$(pwd)":/app api \
     alembic revision --autogenerate -m "Add neues_feld to product"
   ```

    * **Purpose**:

        * Mount your host project into the container so the new file lands in `alembic/versions/`.
        * Compare your updated models against the current DB schema and scaffold a Python migration script.

3. **Review & adjust** the generated script in `alembic/versions/…py`

    * **Purpose**: Catch any edge cases or tweak column properties before applying.

4. **Apply the migration**

   ```bash
   docker compose run --rm -v "$(pwd)":/app api alembic upgrade head
   ```

    * **Purpose**: Execute the migration against Postgres, updating the real database.

5. **Verify**

   ```bash
   docker compose exec db psql -U postgres -d products -c "\d product"
   ```

    * **Purpose**: Confirm the new column or table is present.

---

### 4.3 Automating Migration Application on Startup

If you prefer the container to always auto-apply pending migrations at launch, update your **Dockerfile** `CMD` to:

```dockerfile
CMD ["sh", "-c", "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000"]
```

* **Purpose**:

    1. **`alembic upgrade head`** runs any unapplied migrations.
    2. **`uvicorn ...`** starts the FastAPI server.

> **Reminder**: You still must **manually generate** each migration with `alembic revision`—only the application step is automated.

---

## 5. Summary

* **Docker Compose** handles building, database, and API startup in one command.
* **Git Setup** ensures clean version control and hides credentials.
* **Optional Poetry flow** lets you run directly on the host by pointing at `localhost`.
* **Alembic migrations** version every schema change; you generate them manually and can apply them either manually or automatically at container start.
