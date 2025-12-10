from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.repositories.wallet_repository import WalletRepository
from app.repositories.db import get_db
from app.services.alchemy_trades import fetch_transfers_for_wallet

router = APIRouter(
    prefix="/wallets",
)


@router.get("/all")
def list_wallets(db: Session = Depends(get_db)):
    repo = WalletRepository(db)

    wallets = repo.get_all()

    print(wallets)
    return wallets


@router.get("/{wallet_id}")
def get_wallet(wallet_id: int, db: Session = Depends(get_db)):
    """Returns the data of a chosen wallet by id."""
    repo = WalletRepository(db)
    wallet = repo.get_by_id(wallet_id)

    if wallet is None:
        raise HTTPException(status_code=404, detail="Wallet not found")

    return wallet


@router.get("/{wallet_id}/alchemy-transfers")
def get_wallet_alchemy_transfers(wallet_id: int, db: Session = Depends(get_db)):
    """
    Gets the incoming and outgoing transfers for a specified wallet.
    """
    repo = WalletRepository(db)
    wallet = repo.get_by_id(wallet_id)

    if wallet is None:
        raise HTTPException(status_code=404, detail="Wallet not found")

    if wallet.chain != "ETH":
        raise HTTPException(status_code=400, detail="Only ETH wallets are supported for now")

    incoming = fetch_transfers_for_wallet(wallet, "IN")
    outgoing = fetch_transfers_for_wallet(wallet, "OUT")

    return{
        "wallet_id": wallet.id,
        "address": wallet.address,
        "chain": wallet.chain,
        "incoming_count": len(incoming),
        "outgoing_count": len(outgoing),
        "incoming_trades": incoming[:],
        "outgoing_trades": outgoing[:]
    }
