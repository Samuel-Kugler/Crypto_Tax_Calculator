from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.exceptions.domain import WalletNotFoundException, UnsupportedChainException, DatabaseWriteException


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(WalletNotFoundException)
    async def wallet_not_found_handler(request: Request, exc: WalletNotFoundException):
        return JSONResponse(status_code=404, content={"detail": exc.details})

    @app.exception_handler(UnsupportedChainException)
    async def unsupported_chain_handler(request: Request, exc: UnsupportedChainException):
        return JSONResponse(status_code=400, content={"detail": exc.details})

    @app.exception_handler(DatabaseWriteException)
    async def database_write_exception_handler(request : Request, exc: DatabaseWriteException):
        return JSONResponse(status_code=500, content={"detail": exc.details})
