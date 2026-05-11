from typing import Dict, Any

from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel
from pydantic.json_schema import DEFAULT_REF_TEMPLATE
from sqlalchemy.orm import Session

from app.database import Base, SessionLocal, engine
from app.models import TransactionDB


app = FastAPI(
    title="Finance Tracker API",
    description="A small backend API for tracking personal finance transactions.",
    version="0.1.0",
)


Base.metadata.create_all(bind=engine)


class TransactionCreate(BaseModel):
    date: str
    type: str
    category: str
    amount: float
    note: str | None = None


class TransactionUpdate(BaseModel):
    date: str | None = None
    type: str | None = None
    category: str | None = None
    amount: float | None = None
    note: str | None = None


class Transaction(TransactionCreate):
    id: int

    model_config = {
        "from_attributes": True
    }


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_transaction_or_404(
    transaction_id: int,
    db: Session,
) -> type[TransactionDB]:
    transaction = (
        db.query(TransactionDB)
        .filter(TransactionDB.id == transaction_id)
        .first()
    )

    if transaction is None:
        raise HTTPException(
            status_code=404,
            detail="Transaction not found"
        )

    return transaction


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
def create_transaction(
    transaction: TransactionCreate,
    db: Session = Depends(get_db),
):
    db_transaction = TransactionDB(**transaction.model_dump())

    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)

    return db_transaction


@app.get("/transactions", response_model=list[Transaction])
def get_transactions(
    type: str | None = None,
    category: str | None = None,
    db: Session = Depends(get_db),
):
    query = db.query(TransactionDB)

    if type is not None:
        query = query.filter(TransactionDB.type == type)

    if category is not None:
        query = query.filter(TransactionDB.category == category)

    return query.all()


@app.get("/transactions/{transaction_id}", response_model=Transaction)
def get_transaction(
    transaction_id: int,
    db: Session = Depends(get_db),
):
   return get_transaction_or_404(transaction_id, db)


@app.delete("/transactions/{transaction_id}")
def delete_transaction(
        transaction_id: int,
        db: Session = Depends(get_db),
):
    transaction = get_transaction_or_404(transaction_id, db)

    db.delete(transaction)
    db.commit()

    return {
        "message": "Transaction delete"
    }


@app.patch("/tansactions/{transaction_id}")
def update_transaction(
        transaction_id: int,
        transaction_update: TransactionUpdate,
        db: Session = Depends(get_db),
):
    transaction = get_transaction_or_404(transaction_id, db)

    update_data = transaction_update.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(transaction, field, value)

    db.commit()
    db.refresh(transaction)

    return transaction
