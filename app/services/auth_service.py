from datetime import datetime, timedelta, timezone
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.user import User
from passlib.context import CryptContext
from jose import jwt
import os


pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")
JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

JWT_SECRET = os.getenv("JWT_SECRET")
if not JWT_SECRET:
    raise RuntimeError("JWT_SECRET is missing.")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def register_new_user(email: str, password: str, db: Session) -> dict:
    email_norm = email.strip().lower()

    MIN_PASSWORD_LEN = 8

    if MIN_PASSWORD_LEN > len(password):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"The password length needs to be at least {MIN_PASSWORD_LEN} characters."
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


def verify_password(password: str, password_hash: str) -> bool:
    return pwd_context.verify(password, password_hash)


def create_access_token(user_id: int) -> str:
    expires_at = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    payload = {
        "sub": str(user_id),
        "exp": expires_at,
    }

    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token


def login_user(email: str, password: str, db: Session) -> dict:
    email_norm = email.strip().lower()

    user = db.query(User).filter(User.e_mail_address == email_norm).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Wrong email or password.",
        )

    if not verify_password(password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Wrong email or password.",
        )

    access_token = create_access_token(user_id=user.id)

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }
