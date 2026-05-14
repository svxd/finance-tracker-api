from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.models import TransactionDB
from app.schemas import Transaction, TransactionCreate, TransactionType, TransactionUpdate


router = APIRouter(
    prefix="/transactions",
    tags=["transactions"],
)


def get_transaction_or_404(
    transaction_id: int,
    db: Session,
) -> TransactionDB:
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


@router.post("", response_model=Transaction)
def create_transaction(
    transaction: TransactionCreate,
    db: Session = Depends(get_db),
):
    db_transaction = TransactionDB(**transaction.model_dump())

    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)

    return db_transaction


@router.get("", response_model=list[Transaction])
def get_transactions(
    type: TransactionType | None = None,
    category: str | None = None,
    min_amount: float | None = None,
    max_amount: float | None = None,
    db: Session = Depends(get_db),
):
    if min_amount is not None and max_amount is not None and min_amount > max_amount:
        raise HTTPException(
            status_code=400,
            detail="min_amount cannot be greater than max_amount"
        )

    query = db.query(TransactionDB)

    if type is not None:
        query = query.filter(TransactionDB.type == type)

    if category is not None:
        query = query.filter(TransactionDB.category == category)

    if min_amount is not None:
        query = query.filter(TransactionDB.amount >= min_amount)

    if max_amount is not None:
        query = query.filter(TransactionDB.amount <= max_amount)

    return query.all()


@router.get("/{transaction_id}", response_model=Transaction)
def get_transaction(
    transaction_id: int,
    db: Session = Depends(get_db),
):
    return get_transaction_or_404(transaction_id, db)


@router.patch("/{transaction_id}", response_model=Transaction)
def update_transaction(
    transaction_id: int,
    transaction_update: TransactionUpdate,
    db: Session = Depends(get_db),
):
    transaction = get_transaction_or_404(transaction_id, db)

    update_data = transaction_update.model_dump(exclude_unset=True)

    if not update_data:
        raise HTTPException(
            status_code=400,
            detail="No fields provided for update"
        )

    for field, value in update_data.items():
        setattr(transaction, field, value)

    db.commit()
    db.refresh(transaction)

    return transaction


@router.delete("/{transaction_id}")
def delete_transaction(
    transaction_id: int,
    db: Session = Depends(get_db),
):
    transaction = get_transaction_or_404(transaction_id, db)

    db.delete(transaction)
    db.commit()

    return {
        "message": "Transaction deleted"
    }
