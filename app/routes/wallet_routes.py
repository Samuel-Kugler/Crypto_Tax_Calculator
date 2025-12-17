from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.repositories.wallet_repository import WalletRepository
from app.repositories.db import get_db

router = APIRouter(
    prefix="/wallets",
)


@router.get("/all")
def list_wallets(db: Session = Depends(get_db)):
    repo = WalletRepository(db)

    wallets = repo.get_all()

    print(wallets)
    return wallets


@router.get("/{wallet_id}")
def get_wallet(wallet_id: int, db: Session = Depends(get_db)):
    """Returns the data of a chosen wallet by id."""
    repo = WalletRepository(db)
    wallet = repo.get_by_id(wallet_id)

    if wallet is None:
        raise HTTPException(status_code=404, detail="Wallet not found")

    return wallet
