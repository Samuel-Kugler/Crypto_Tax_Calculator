from sqlalchemy.orm import Session

from app.exceptions.domain import WalletNotFoundException, UnsupportedChainException
from app.repositories.wallet_repository import WalletRepository
from app.clients.alchemy_client import fetch_transfers_for_wallet


def get_all_trades(wallet_id: int, db: Session):
    repo = WalletRepository(db)
    wallet = repo.get_by_id(wallet_id)

    if wallet is None:
        raise WalletNotFoundException("This wallet doesn't exist.")

    if wallet.chain != "ETH":
        raise UnsupportedChainException(wallet.chain)

    incoming = fetch_transfers_for_wallet(wallet, "IN")
    outgoing = fetch_transfers_for_wallet(wallet, "OUT")

    return {
        "wallet_id": wallet.id,
        "address": wallet.address,
        "chain": wallet.chain,
        "incoming_count": len(incoming),
        "outgoing_count": len(outgoing),
        "incoming_trades": incoming,
        "outgoing_trades": outgoing,
    }


#speichern in der Datenbank -> update des service namens zu update wallet
