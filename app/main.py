from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel
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
def get_transactions(db: Session = Depends(get_db)):
    return db.query(TransactionDB).all()


@app.get("/transactions/{transaction_id}", response_model=Transaction)
def get_transaction(
    transaction_id: int,
    db: Session = Depends(get_db),
):
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