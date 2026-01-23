from sqlalchemy.orm import Session
from app.models.user import User


class UserRepository():
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return (
            self.db
            .query(User)
            .order_by(User.e_mail_address.asc())
            .all()
            )

    def get_by_id(self, user_id: int) -> User | None:
        return self.db.query(User).filter(User.id == user_id).first()

    def get_by_email(self, e_mail_address: str) -> User | None:
        return self.db.query(User).filter(User.e_mail_address == e_mail_address).first()
