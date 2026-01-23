from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.repositories.db import get_db
from app.services.user_service import get_users

router = APIRouter(
    prefix="/users",
    tags=["users"]
)


@router.get("/all_users")
def list_users(db: Session = Depends(get_db)):
    return get_users(db)
