from fastapi import HTTPException
from pydantic import BaseModel
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app.exceptions.domain import WalletNotFoundException
from app.models.enums import BlockchainEnum
from app.repositories.wallet_repository import WalletRepository


class WalletCreate(BaseModel):
    address: str
    chain: BlockchainEnum
    name: str | None = None


def list_wallets(db: Session, user_id: int):
    repo = WalletRepository(db)
    return repo.get_all_for_user(user_id)


def get_wallet_by_id(wallet_id: int, db: Session, user_id: int):
    repo = WalletRepository(db)
    wallet = repo.get_by_id_for_user(wallet_id=wallet_id, user_id=user_id)

    if wallet is None:
        raise WalletNotFoundException("Wallet not found")

    return wallet


def create_wallet(db: Session, user_id: int, data: WalletCreate):
    repo = WalletRepository(db)

    address = data.address.strip().lower()

    try:
        wallet = repo.create_wallet_for_user(
            user_id=user_id,
            address=address,
            chain=data.chain,
            name=data.name,
        )
        db.commit()
        db.refresh(wallet)
        return wallet

    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Wallet already exists")
