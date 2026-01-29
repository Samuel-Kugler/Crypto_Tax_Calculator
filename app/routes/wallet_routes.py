from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies.auth import get_current_user
from app.models.user import User
from app.repositories.db import get_db
from app.services.update_wallet import update_wallet
from app.services.wallet_service import list_wallets, get_wallet_by_id
from app.services.wallet_service import WalletCreate, create_wallet


router = APIRouter(
    prefix="/wallets",
    tags=["wallets"]
)


@router.get("")
def get_all_wallets(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return list_wallets(db=db, user_id=current_user.id)


@router.get("/{wallet_id}")
def get_wallet_route(
    wallet_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_wallet_by_id(wallet_id=wallet_id, db=db, user_id=current_user.id)


@router.post("/{wallet_id}/update_wallet")
def update_wallet_route(
    wallet_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return update_wallet(wallet_id=wallet_id, user_id=current_user.id, db=db)


@router.post("")
def create_wallet_route(
    data: WalletCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return create_wallet(db, user_id=current_user.id, data=data)



