from sqlalchemy.orm import Session
from app.models.wallet import Wallet


class WalletRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return (
            self.db
            .query(Wallet)
            .order_by(Wallet.id)
            .all()
        )

    def get_by_id(self, wallet_id: int) -> Wallet | None:
        return (
            self.db
            .query(Wallet)
            .filter(Wallet.id == wallet_id)
            .first()
        )
