from dotenv import load_dotenv
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker


load_dotenv()


url = os.getenv("DATABASE_URL")
if not url:
    raise RuntimeError("DATABASE_URL is missing")

if url.startswith("postgres://"):
    url = url.replace("postgres://", "postgresql://", 1)

if "sslmode=" not in url:
    if "?" in url:
        url = url + "&sslmode=require"
    else:
        url = url + "?sslmode=require"


engine = create_engine(
    url,
    pool_pre_ping=True,
    pool_recycle=1800
)

Base = declarative_base()

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
