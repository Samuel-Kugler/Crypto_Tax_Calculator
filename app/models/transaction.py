from sqlalchemy import Column, Integer, Text, Numeric, ForeignKey, func, TIMESTAMP, UniqueConstraint, BigInteger
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import relationship

from app.repositories.db import Base
from app.models.enums import DirectionEnum


class Transaction(Base):
    __tablename__ = "transaction"

    id = Column(BigInteger, primary_key=True, index=True)

    wallet_id = Column(
        Integer,
        ForeignKey("wallet.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    tx_hash = Column(Text, nullable=False, index=True)

    direction = Column(
        ENUM(DirectionEnum,
             name="direction_enum",
             create_type=False,
             validate_strings=True
             ),
        nullable=False
    )

    asset_symbol = Column(Text, nullable=False)

    amount = Column(
        Numeric(38, 18),
        nullable=False
    )

    fee_amount = Column(
        Numeric(38, 18),
        nullable=True
    )

    fee_asset_symbol = Column(Text, nullable=True)

    occurred_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False
    )

    imported_at = Column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    source = Column(Text, nullable=False)

    note = Column(Text, nullable=True)

    wallet = relationship("Wallet", back_populates="transactions")

    from_address = Column(Text, nullable=False, index=True)

    to_address = Column(Text, nullable=False, index=True)

    chain = Column(Text, nullable=False)

    __table_args__ = (
        UniqueConstraint("wallet_id", "tx_hash", name="uq_transaction_wallet_txhash"),
    )

