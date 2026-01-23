from sqlalchemy.orm import Session

from app.repositories.user_repository import UserRepository


def get_users(db: Session):
    repo = UserRepository(db)

    users = repo.get_all()

    return users
