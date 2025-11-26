from sqlalchemy import text
from app.repositories.db import engine


class WalletRepository:

    def get_all(self):
        with engine.connect() as conn:
            rows = conn.execute(
                text("SELECT * FROM wallets ORDER BY id")
            ).mappings().all()

            return [dict(r) for r in rows]
