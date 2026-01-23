from warnings import deprecated

from fastapi import HTTPException, status
from pydantic import EmailStr
from sqlalchemy.orm import Session
from app.models.user import User
from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def register_new_user(email: str, password: str, db: Session) -> dict:
    email_norm = email.strip().lower()

    MIN_PASSWORD_LEN = 8
    MAX_PASSWORD_LEN = 72

    if MIN_PASSWORD_LEN > len(password) > MAX_PASSWORD_LEN:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"The password length needs to be between {MIN_PASSWORD_LEN} and {MAX_PASSWORD_LEN} characters."
        )

    existing_user = db.query(User).filter(User.e_mail_address == email_norm).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Email {email_norm} already registered."
        )

    password_hash = hash_password(password)

    new_user = User(
        e_mail_address=email_norm,
        password_hash=password_hash,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "id": new_user.id,
        "e_mail": new_user.e_mail_address,
        "created_at": new_user.created_at
    }
