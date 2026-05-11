from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(
    title="Finance Tracker API",
    description="A small backend API for tracking personal finance transactions.",
    version="0.1.0",
)


class TransactionCreate(BaseModel):
    date: str
    type: str
    category: str
    amount: float
    note: str | None = None


class Transaction(TransactionCreate):
    id: int


transactions: list[Transaction] = []
next_transaction_id = 1


@app.get("/")
def read_root():
    return {
        "message": "Finance Tracker API is running",
    }


@app.get("/health")
def health_check():
    return {
        "status": "ok"
    }


@app.get("/version")
def version_check():
    return {
        "version": "0.1.0"
    }


@app.get("/about")
def about_info():
    return {
        "project": "Finance Tracker API",
        "purpose": "Backend sprint project for learning FastAPI"
    }


@app.post("/transactions", response_model=Transaction)
def create_transaction(transaction: TransactionCreate):
    global next_transaction_id

    new_transaction = Transaction(
        id=next_transaction_id,
        **transaction.model_dump()
    )

    transactions.append(new_transaction)
    next_transaction_id += 1

    return new_transaction


@app.get("/transactions", response_model=list[Transaction])
def get_transactions():
    return transactions


@app.get("/transactions/{transaction_id}", response_model=Transaction)
def get_transaction(transaction_id: int):
    for transaction in transactions:
        if transaction.id == transaction_id:
            return transaction

    raise HTTPException(
        status_code=404,
        detail="Transaction not found"
    )
