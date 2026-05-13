# Finance Tracker API

Small backend API project for learning FastAPI, CRUD, databases, testing and simple finance analytics.

## Current status

The project currently supports basic transaction CRUD operations, SQLite persistence, and simple filtering.

## Progress

### Day 1 — FastAPI basics

- FastAPI app created
- Root endpoint added
- Health endpoint added
- Version/about endpoints added

### Day 2 — In-memory transactions API

- Added transaction creation
- Added transaction list endpoint
- Added transaction detail endpoint
- Added 404 handling for missing transactions
- Used temporary in-memory storage

### Day 3 — SQLite persistence

- Added SQLite database persistence with SQLAlchemy
- Removed in-memory list storage
- Added SQLAlchemy ORM model
- Added database session management through FastAPI dependencies

New files:

```text
app/database.py
app/models.py
```

### Day 4 — CRUD and filters

- Added transaction filtering by type and category
- Added transaction deletion
- Added partial transaction update with PATCH
- Added shared helper for 404 handling

Notes:

- PATCH supports explicit `null` for optional fields like `note`
- If a field is not provided in PATCH body, it is not changed

### Day 5 — Validation and better filters

- Added validation for transaction type
- Added positive amount validation
- Added non-empty category validation
- Added empty PATCH protection
- Added amount range filters
- Added validation for amount range filters

New filters:

```text
GET /transactions?min_amount=1000
GET /transactions?max_amount=50000
GET /transactions?min_amount=1000&max_amount=50000
```

### Day 6 — Date validation and finance summaries

- Added real date validation
- Changed transaction date from string to date type
- Added total finance summary endpoint
- Added expense summary by category endpoint

New endpoints:

```text
GET /summary
GET /summary/categories
```

net = income - expenses
transfers are not included in net because they represent internal money movement

## Project structure

```text
finance-tracker-api/
  app/
    main.py
    database.py
    models.py
  requirements.txt
  README.md
```

## Database

SQLite database file:

```text
finance.db
```

Transactions are stored in SQLite and persist after server restart.

The local database file should not be committed to Git.

## Endpoints

```text
GET    /
GET    /health
GET    /version
GET    /about

POST   /transactions
GET    /transactions
GET    /transactions?type=expense
GET    /transactions?category=Вело-покупки
GET    /transactions?type=expense&category=Вело-покупки
GET    /transactions/{transaction_id}
PATCH  /transactions/{transaction_id}
DELETE /transactions/{transaction_id}
GET    /transactions?min_amount=1000
GET    /transactions?max_amount=50000
GET    /transactions?min_amount=1000&max_amount=50000
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
net = income - expenses
transfers are not included in net because they represent internal money movement
## Run locally

Create and activate virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

Run server:

```bash
uvicorn app.main:app --reload
```

## Docs

After running the server, open:

```text
http://127.0.0.1:8000/docs
```

## Notes

This is a learning backend project.

Current focus:

- FastAPI basics
- CRUD operations
- SQLite persistence
- SQLAlchemy ORM
- API validation and error handling

Next planned steps:

- Better validation rules
- Cleaner project structure
- Routers
- Tests
- Simple finance analytics endpoints
- 