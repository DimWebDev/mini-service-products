Your **Docker** instructions are spot-on for the “container-only” workflow—everything will build, start Postgres, auto-create your tables via the startup hook and expose FastAPI on port 8000. The **Poetry** section, as written, will still fail out-of-the-box because your `.env` points at `db:5432`, which only resolves inside the Docker network. If you truly only ever want to work with the container, you can simplify your README to:

````markdown
## Running the App

### Via Docker Compose

This builds the API image, starts Postgres and your FastAPI service, auto-creates tables on startup, and serves at http://localhost:8000:

```bash
docker compose up --build
````

Once you see

```
api_1  | INFO:     Uvicorn running on http://0.0.0.0:8000
```

you can exercise the endpoints, for example:

```bash
curl -X POST http://localhost:8000/products \
     -H "Content-Type: application/json" \
     -d '{"name":"Widget","price":19.99}'
curl http://localhost:8000/products
```

---

## Git Setup

```bash
git init
echo ".env" >> .gitignore
git add .
git commit -m "Initial commit: containerized FastAPI + Postgres scaffold"
```

1. **`git init`** creates a new repo.
2. **`.env`** is ignored so you never commit credentials.
3. **`git add .`** stages all your code.
4. **`git commit`** records your starting point.

---

### (Optional) Local “Poetry” invocation

If you do ever want to run Uvicorn on your host (instead of in Docker), you must point `DATABASE_URL` at `localhost`, not `db`. One approach is:

```bash
# 1. Start only Postgres in Docker
docker compose up -d db

# 2. Create a file `.env.local`:
#    DATABASE_URL=postgresql+psycopg2://postgres:postgres@localhost:5432/products

# 3. Launch the app loading that file:
poetry run dotenv run --file .env.local -- uvicorn app.main:app --reload
```

But if “container only” is your goal, you can safely omit this section.
