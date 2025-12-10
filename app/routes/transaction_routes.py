from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.repositories.transaction_repository import TransactionRepository
from app.repositories.db import get_db

router = APIRouter(
    prefix="/transactions",
)


@router.get("/all")
def list_wallets(db: Session = Depends(get_db)):
    repo = TransactionRepository(db)

    transactions = repo.get_all()

    print(transactions)
    return transactions
