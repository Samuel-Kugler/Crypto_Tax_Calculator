from sqlalchemy import Column, Integer, Text, TIMESTAMP, func, text, ForeignKey, BigInteger
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import relationship

from app.repositories.db import Base
from app.models.enums import BlockchainEnum, ActivityEnum


class Wallet(Base):
    __tablename__ = "wallet"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    address = Column(
        Text,
        nullable=False
    )

    chain = Column(
        ENUM(
            BlockchainEnum,
            name="blockchain_enum",
            create_type=False,
            validate_strings=True
        ),
        nullable=False
    )

    name = Column(
        Text,
        nullable=True
    )

    created_at = Column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    last_synced_at = Column(
        TIMESTAMP(timezone=True),
        nullable=True
    )

    status = Column(
        ENUM(
            ActivityEnum,
            name="activity_enum",
            create_type=False,
            validate_strings=True
        ),
        server_default=text("'active'"),
        nullable=False
    )

    user_id = Column(
        BigInteger,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    user = relationship("User", back_populates="wallets")

    transactions = relationship(
        "Transaction",
        back_populates="wallet",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

