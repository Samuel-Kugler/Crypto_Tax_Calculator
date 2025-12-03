from sqlalchemy.orm import Session
from app.models.wallet_models import Wallet


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
