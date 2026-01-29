from sqlalchemy.orm import Session
from app.models.wallet import Wallet


class WalletRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all_for_user(self, user_id: int):
        return (
            self.db
            .query(Wallet)
            .filter(Wallet.user_id == user_id)
            .order_by(Wallet.id)
            .all()
        )

    def get_by_id_for_user(self, wallet_id: int, user_id: int) -> Wallet | None:
        return (
            self.db
            .query(Wallet)
            .filter(Wallet.id == wallet_id, Wallet.user_id == user_id)
            .first()
        )
