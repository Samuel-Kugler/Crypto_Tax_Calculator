from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.repositories.wallet_repository import WalletRepository
from app.repositories.db import get_db

router = APIRouter(
    prefix="/wallets",
)


@router.get("/")
def list_wallets(db: Session = Depends(get_db)):
    repo = WalletRepository(db)

    wallets = repo.get_all()

    print(wallets)
    return wallets

