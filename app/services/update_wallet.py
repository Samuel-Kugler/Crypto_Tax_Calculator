from typing import Any

from sqlalchemy.orm import Session

from app.exceptions.domain import WalletNotFoundException, UnsupportedChainException
from app.models.enums import DirectionEnum
from app.repositories.wallet_repository import WalletRepository
from app.clients.alchemy_client import fetch_transfers_for_wallet


def normalize_alchemy_transfers(wallet_id: int, trades: list[dict]) -> list[dict[str, Any]]:
    result = []

    for trade in trades:
        new_row = {
            "wallet_id": wallet_id,
            "tx_hash":  trade.get("hash"),
            "direction":
        }



def get_all_trades(wallet_id: int, db: Session):
    repo = WalletRepository(db)
    wallet = repo.get_by_id(wallet_id)

    if wallet is None:
        raise WalletNotFoundException("This wallet doesn't exist.")

    if wallet.chain != "ETH":
        raise UnsupportedChainException(wallet.chain)

    incoming = fetch_transfers_for_wallet(wallet, "IN")
    normalized_incoming_trades = normalize_alchemy_transfers(wallet_id, "IN",incoming)

    outgoing = fetch_transfers_for_wallet(wallet, "OUT")
    normalized_outgoing_trades = normalize_alchemy_transfers(wallet_id, "OUT", outgoing)

    return incoming
