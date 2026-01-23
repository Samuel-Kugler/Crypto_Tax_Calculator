from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies.auth import get_current_user
from app.models.user import User
from app.models.wallet import Wallet
from app.repositories.db import get_db
from app.services.update_wallet import update_wallet
from app.services.wallet_service import list_wallets, get_wallet_by_id

router = APIRouter(
    prefix="/wallets",
    tags=["wallets"]
)


@router.get("/all")
def get_all_wallets(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return db.query(Wallet).filter(Wallet.user_id == current_user.id).all()


@router.get("/{wallet_id}")
def get_wallet_route(wallet_id: int, db: Session = Depends(get_db)):
    return get_wallet_by_id(wallet_id=wallet_id, db=db)


@router.get("/{wallet_id}/update_wallet")
def get_number_of_new_transfers(wallet_id: int, db: Session = Depends(get_db)):
    return update_wallet(wallet_id=wallet_id, db=db)


