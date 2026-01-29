from typing import Any
import logging

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.exceptions.domain import WalletNotFoundException, UnsupportedChainException, DatabaseWriteException
from app.repositories.wallet_repository import WalletRepository
from app.repositories.transaction_repository import TransactionRepository
from app.clients.alchemy_client import fetch_transfers_for_wallet
from datetime import datetime, timezone

logger = logging.getLogger(__name__)


def normalize_time(time_value) -> datetime | None:
    """
    "blockTimestamp": "2020-12-13T19:03:53.000Z"
    """
    if not time_value or not isinstance(time_value, str):
        return None

    time_value = time_value.strip()
    if time_value.endswith("Z"):
        time_value = time_value[:-1] + "+00:00"

    try:
        dt = datetime.fromisoformat(time_value)
    except ValueError:
        return None

    return dt


def normalize_alchemy_transfers(wallet_id: int, trades: list[dict], direction: str, chain: str) -> list[dict[str, Any]]:
    result = []

    for trade in trades:
        metadata = trade.get("metadata") or {}
        occurred_at = normalize_time(metadata.get("blockTimestamp"))
        asset_symbol = trade.get("asset") or "UNKNOWN"
        amount = trade.get("value") or 0

        new_row = {
            "wallet_id": wallet_id,
            "tx_hash":  trade.get("hash"),
            "direction": direction,
            "asset_symbol": asset_symbol,
            "amount": amount,
            "fee_amount": None,
            "fee_asset_symbol": None,
            "occurred_at": occurred_at,
            "imported_at": datetime.now(timezone.utc),
            "source": "alchemy",
            "note": None,
            "from_address": trade.get("from"),
            "to_address": trade.get("to"),
            "chain": chain,
            "alchemy_unique_id": trade.get("uniqueId")
        }
        result.append(new_row)

    return result


def get_all_trades(wallet_id: int, user_id: int, db: Session):
    repo = WalletRepository(db)
    wallet = repo.get_by_id_for_user(wallet_id=wallet_id, user_id=user_id)

    if wallet is None:
        raise WalletNotFoundException("This wallet doesn't exist.")

    if wallet.chain != "ETH":
        raise UnsupportedChainException(wallet.chain)

    for page in fetch_transfers_for_wallet(wallet, "IN"):
        yield normalize_alchemy_transfers(wallet_id, page, "IN", chain=wallet.chain)

    for page in fetch_transfers_for_wallet(wallet, "OUT"):
        yield normalize_alchemy_transfers(wallet_id, page, "OUT", chain=wallet.chain)


def update_wallet(wallet_id: int, user_id: int, db: Session) -> dict:
    transaction_repository = TransactionRepository(db)

    fetched_count = 0
    inserted_transactions_counter = 0

    try:
        for rows_page in get_all_trades(wallet_id=wallet_id, user_id=user_id, db=db):
            fetched_count += len(rows_page)

            inserted_transactions_counter += transaction_repository.bulk_insert_ignore_duplicates(rows_page)

            db.commit()

    except SQLAlchemyError as e:
        db.rollback()
        logger.exception("DB error while inserting transactions")
        raise DatabaseWriteException() from e

    return {
        "wallet_id": wallet_id,
        "fetched": fetched_count,
        "inserted": inserted_transactions_counter
    }

