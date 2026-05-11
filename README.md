# Finance Tracker API

Small backend API project for learning FastAPI, CRUD, databases, testing and simple finance analytics.

## Current status

### Day 1

- FastAPI app created
- health endpoint added
- root endpoint added
- version/about endpoints added

### Day 2

- Added in-memory transactions API
- Added transaction creation
- Added transaction list endpoint
- Added transaction detail endpoint
- Added 404 handling for missing transaction

### Day 3

Added SQLite database persistence with SQLAlchemy.

### New files

```text
app/database.py
app/models.py
```

### What changed

- Transactions are now stored in SQLite database.
- In-memory list storage was removed.
- SQLAlchemy ORM model was added.
- Database sessions are managed through FastAPI dependencies.

### Database

SQLite database file:

```text
finance.db
```

Transactions now persist after server restart.

## Endpoints

```text
GET /
GET /health
GET /version
GET /about
POST /transactions
GET /transactions
GET /transactions/{transaction_id}
```

## Example transaction

```json
{
  "date": "2026-04-20",
  "type": "expense",
  "category": "Вело-покупки",
  "amount": 42000,
  "note": "Велоформа"
}
```

## Run locally

```bash
source .venv/bin/activate
uvicorn app.main:app --reload
```

## Docs

After running the server, open:

```text
http://127.0.0.1:8000/docs
```

## Notes

Transactions are currently stored in memory.

They will be lost after server restart. Database support will be added later.