from dotenv import load_dotenv
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
load_dotenv()


url = os.getenv("DATABASE_URL")
if not url:
    raise RuntimeError("DATABASE_URL is missing")

engine = create_engine(
    url,
    echo=True,
    future=True
)

session = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


def get_db():
    """
    Opens a new session and closes it automatically afterward
    :return:
    """
    db = session()
    try:
        yield db
    finally:
        db.close()
