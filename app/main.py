from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from app.routes.wallet_routes import router as wallet_router

#uvicorn app.main:app --reload
app = FastAPI()
app.include_router(wallet_router)


@app.get("/", response_class=HTMLResponse)
def index():
    return """
    <h1>Welcome!</h1>
    <p>
        <a href="http://127.0.0.1:8000/wallets">➡️ Zu den Wallets</a>
    </p>
    """



