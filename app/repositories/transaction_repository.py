from typing import Any
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session

from app.models.transaction import Transaction


class TransactionRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return (
            self.db.query(Transaction)
            .order_by(Transaction.wallet_id.asc(), Transaction.occurred_at.desc())
            .all()
        )

    def get_by_wallet(self, wallet_id: int):
        return (
            self.db.query(Transaction)
            .filter(Transaction.wallet_id == wallet_id)
            .order_by(Transaction.occurred_at.asc())
            .all()
        )

    def bulk_insert_ignore_duplicates(self, rows: list[dict[str, Any]]) -> int:
        if not rows:
            return 0

        statement = insert(Transaction).values(rows)
        statement = statement.on_conflict_do_nothing(
            index_elements=["wallet_id", "alchemy_unique_id"]
        )
        statement = statement.returning(Transaction.id)

        result = self.db.execute(statement)
        inserted_transactions = result.scalars().all()

        return len(inserted_transactions)
