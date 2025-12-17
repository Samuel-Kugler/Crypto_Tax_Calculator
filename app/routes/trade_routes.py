from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.repositories.db import get_db
from app.services.trade_service import get_all_trades

router = APIRouter(
    prefix="/trades"
)


@router.get("/{wallet_id}/transfers")
def get_wallet_transfers(wallet_id: int, db: Session = Depends(get_db)):
    return get_all_trades(wallet_id=wallet_id, db=db)
