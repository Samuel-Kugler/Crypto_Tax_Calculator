from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from app.routes.wallet_routes import router as wallet_router
from app.routes.transaction_routes import router as transaction_router
from app.repositories.db import Base, engine  # noqa
from app.models import wallet, transaction  # noqa

#uvicorn app.main:app --reload
app = FastAPI()
app.include_router(wallet_router)
app.include_router(transaction_router)


@app.get("/", response_class=HTMLResponse)
def index():
    return """
    <h1>Welcome!</h1>
    <p>
        <a href="http://127.0.0.1:8000/wallets/all">➡️ All wallets</a>
        <br>
        <a href="http://127.0.0.1:8000/transactions/all">➡️ All transactions</a>
        <br>
        <a href="http://127.0.0.1:8000/wallets/1/alchemy-transfers"➡️ example for wallet 1</a>
    </p>
    """
