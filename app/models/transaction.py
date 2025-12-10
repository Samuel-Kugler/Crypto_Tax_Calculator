from sqlalchemy import Column, Integer, Text, Numeric, ForeignKey, func, TIMESTAMP
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import relationship

from app.repositories.db import Base
from app.models.enums import DirectionEnum


class Transaction(Base):
    __tablename__ = "transaction"

    id = Column(Integer, primary_key=True, index=True)

    wallet_id = Column(
        Integer,
        ForeignKey("wallet.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    tx_hash = Column(Text, nullable=True)

    direction = Column(
        ENUM(DirectionEnum,
             name="direction_enum",
             create_type=False,
             validate_strings=True
             ),
        nullabla=False
    )

    asset_symbol = Column(Text, nullable=False)

    amount = Column(
        Numeric(38, 18),
        nullable=False
    )

    fee_amount = Column(
        Numeric(38, 18),
        nullable=False
    )

    fee_asset_symbol = Column(Text, nullable=False)

    occurred_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False
    )

    imported_at = Column(
        TIMESTAMP(timezone=True),
        serfer_default=func.now(),
        nullable=False
    )

    source = Column(Text, nullable=False)

    note = Column(Text, nullable=True)

    wallet = relationship("Wallet", back_populates="transactions")
