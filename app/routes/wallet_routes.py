from fastapi import APIRouter
from app.repositories.wallet_repository import WalletRepository

router = APIRouter()


@router.get("/wallets")
def test_wallet_route():
    repository = WalletRepository()
    wallets = repository.get_all()
    return wallets


