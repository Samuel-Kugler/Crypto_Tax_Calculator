from sqlalchemy.orm import Session

from app.repositories.transaction_repository import TransactionRepository


def get_transactions(db: Session):
    repo = TransactionRepository(db)

    transactions = repo.get_all()

    return transactions
