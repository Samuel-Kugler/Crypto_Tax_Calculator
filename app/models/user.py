from sqlalchemy import Column, BigInteger, Text, TIMESTAMP, func
from sqlalchemy.orm import relationship

from app.repositories.db import Base


class User(Base):
    __tablename__ = "users"

    id = Column(
        BigInteger,
        primary_key=True,
        index=True
    )

    e_mail_address = Column(
        Text,
        nullable=False,
        unique=True
    )

    password_hash = Column(
        Text,
        nullable=False
    )

    last_login = Column(
        TIMESTAMP(timezone=True),
        nullable=True
    )

    created_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=func.now()
    )

    wallets = relationship(
        "Wallet",
        back_populates="user",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
