from sqlalchemy import Column, Integer, Text, TIMESTAMP, func, text
from sqlalchemy.dialects.postgresql import ENUM

from app.repositories.db import Base


class Wallet(Base):
    __tablename__ = "wallets"

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
        ENUM(name="blockchain_enum"),
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
        ENUM(name="activity_enum"),
        server_default=text("'active'"),
        nullable=False
    )
