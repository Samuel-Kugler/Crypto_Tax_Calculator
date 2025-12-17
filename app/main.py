from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse

from app.routes.wallet_routes import router as wallet_router
from app.routes.transaction_routes import router as transaction_router
from app.routes.trade_routes import router as trade_router
from app.handlers.exception_handlers import register_exception_handlers
from app.repositories.db import Base, engine  # noqa
from app.models import wallet, transaction  # noqa


app = FastAPI(title="Crypto Tax Calculator")
register_exception_handlers(app)

# Routers
app.include_router(wallet_router)
app.include_router(transaction_router)
app.include_router(trade_router)


@app.get("/", response_class=HTMLResponse)
def index():
    return """
    <h1>Welcome!</h1>
    <p>
        <a href="http://127.0.0.1:8000/wallets/all">➡️ All wallets</a>
        <br>
        <a href="http://127.0.0.1:8000/transactions/all">➡️ All transactions</a>
        <br>
        <a href="http://127.0.0.1:8000/trades/1/transfers">➡️ transfers for wallet 1</a>
    </p>
    """
