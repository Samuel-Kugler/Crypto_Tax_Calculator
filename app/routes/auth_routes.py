from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session

from app.repositories.db import get_db
from app.services.auth_service import register_new_user, login_user
router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str


@router.post("/register")
def register_user(
        data: RegisterRequest,
        db: Session = Depends(get_db)
):
    return register_new_user(
        email=str(data.email),
        password=data.password,
        db=db
    )


@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    return login_user(
        email=form_data.username,
        password=form_data.password,
        db=db
    )

