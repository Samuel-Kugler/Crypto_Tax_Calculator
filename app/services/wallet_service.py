from sqlalchemy.orm import Session

from app.exceptions.domain import WalletNotFoundException
from app.repositories.wallet_repository import WalletRepository


def list_wallets(db: Session):
    repo = WalletRepository(db)
    return repo.get_all()


def get_wallet_by_id(wallet_id: int, db: Session):
    repo = WalletRepository(db)
    wallet = repo.get_by_id(wallet_id)

    if wallet is None:
        raise WalletNotFoundException("Wallet not found")

    return wallet
