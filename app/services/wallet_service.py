from sqlalchemy.orm import Session
from app.exceptions.domain import WalletNotFoundException
from app.repositories.wallet_repository import WalletRepository


def list_wallets(db: Session, user_id: int):
    repo = WalletRepository(db)
    return repo.get_all_for_user(user_id)


def get_wallet_by_id(wallet_id: int, db: Session, user_id: int):
    repo = WalletRepository(db)
    wallet = repo.get_by_id_for_user(wallet_id=wallet_id, user_id=user_id)

    if wallet is None:
        raise WalletNotFoundException("Wallet not found")

    return wallet
