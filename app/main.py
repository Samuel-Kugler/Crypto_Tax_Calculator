from fastapi import FastAPI

from app.routes.wallet_routes import router as wallet_router
from app.routes.transaction_routes import router as transaction_router
from app.routes.user_routes import router as user_router
from app.routes.auth_routes import router as auth_router
from app.handlers.exception_handlers import register_exception_handlers
from app.repositories.db import Base, engine  # noqa
from app.models import wallet, transaction, user  # noqa


#uvicorn app.main:app --reload
app = FastAPI(title="Crypto Tax Calculator")
register_exception_handlers(app)

# Routers
app.include_router(wallet_router)
app.include_router(transaction_router)
app.include_router(user_router)
app.include_router(auth_router)

