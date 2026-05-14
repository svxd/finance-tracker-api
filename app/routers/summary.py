from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.models import TransactionDB


router = APIRouter(
    prefix="/summary",
    tags=["summary"],
)


@router.get("")
def get_summary(
    db: Session = Depends(get_db),
):
    total_income = (
        db.query(func.sum(TransactionDB.amount))
        .filter(TransactionDB.type == "income")
        .scalar()
    ) or 0

    total_expenses = (
        db.query(func.sum(TransactionDB.amount))
        .filter(TransactionDB.type == "expense")
        .scalar()
    ) or 0

    total_transfers = (
        db.query(func.sum(TransactionDB.amount))
        .filter(TransactionDB.type == "transfer")
        .scalar()
    ) or 0

    transactions_count = (
        db.query(func.count(TransactionDB.id))
        .scalar()
    ) or 0

    net = total_income - total_expenses

    return {
        "total_income": total_income,
        "total_expenses": total_expenses,
        "total_transfers": total_transfers,
        "net": net,
        "transactions_count": transactions_count,
    }


@router.get("/categories")
def get_summary_categories(
    db: Session = Depends(get_db),
):
    rows = (
        db.query(
            TransactionDB.category,
            func.sum(TransactionDB.amount).label("total"),
            func.count(TransactionDB.id).label("count"),
        )
        .filter(TransactionDB.type == "expense")
        .group_by(TransactionDB.category)
        .order_by(func.sum(TransactionDB.amount).desc())
        .all()
    )

    return [
        {
            "category": row.category,
            "total": row.total,
            "count": row.count,
        }
        for row in rows
    ]
