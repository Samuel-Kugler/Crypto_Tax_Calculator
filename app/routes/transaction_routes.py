from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.services.transaction_service import get_transactions
from app.repositories.db import get_db

router = APIRouter(
    prefix="/transactions",
    tags=["transactions"]
)


@router.get("/all_transactions")
def list_wallets(db: Session = Depends(get_db)):
    return get_transactions(db=db)


