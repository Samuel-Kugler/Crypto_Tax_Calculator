from dotenv import load_dotenv
import os
from sqlalchemy import create_engine
load_dotenv()


url = os.getenv("DATABASE_URL")
if not url:
    raise RuntimeError("DATABASE_URL is missing")

engine = create_engine(
    url,
    pool_pre_ping=True,
    pool_recycle=1800
)


