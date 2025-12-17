from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.repositories.db import get_db
from app.services.wallet_service import list_wallets, get_wallet_by_id

router = APIRouter(
    prefix="/wallets",
    tags=["wallets"]
)


@router.get("/all")
def list_wallets_route(db: Session = Depends(get_db)):
    return list_wallets(db=db)


@router.get("/{wallet_id}")
def get_wallet_route(wallet_id: int, db: Session = Depends(get_db)):
    return get_wallet_by_id(wallet_id=wallet_id, db=db)
