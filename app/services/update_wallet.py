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


def get_all_trades(wallet_id: int, db: Session):
    repo = WalletRepository(db)
    wallet = repo.get_by_id(wallet_id)

    if wallet is None:
        raise WalletNotFoundException("This wallet doesn't exist.")

    if wallet.chain != "ETH":
        raise UnsupportedChainException(wallet.chain)

    incoming = fetch_transfers_for_wallet(wallet, "IN")
    normalized_incoming_trades = normalize_alchemy_transfers(wallet_id, incoming, "IN", chain=wallet.chain)

    outgoing = fetch_transfers_for_wallet(wallet, "OUT")
    normalized_outgoing_trades = normalize_alchemy_transfers(wallet_id, outgoing, "OUT", chain=wallet.chain)

    return normalized_incoming_trades + normalized_outgoing_trades


def update_wallet(wallet_id:int, db: Session) -> dict:
    try:
        rows = get_all_trades(wallet_id, db=db)

        transaction_repository = TransactionRepository(db)
        inserted_transactions_counter = transaction_repository.bulk_insert_ignore_duplicates(rows)

        db.commit()
    except SQLAlchemyError as e:
        db.rollback()
        logger.exception("DB error while inserting transactions")
        raise DatabaseWriteException() from e

    fetched_count = len(rows)

    return {
        "wallet_id": wallet_id,
        "fetched": fetched_count,
        "inserted": inserted_transactions_counter
    }
