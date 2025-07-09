from fastapi import Request, HTTPException, Depends
from app.core.security import verify_token
from app.models.user import User
from app.db.database import SessionLocal
from sqlalchemy.orm import Session
from typing import Generator


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(request: Request, db: Session = Depends(get_db)) -> User:
    token = request.headers.get("Authorization")
    if not token:
        raise HTTPException(status_code=401, detail="Missing token")

    if not token.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid token format")

    try:
        token = token[7:]  # Remove "Bearer "
        username = verify_token(token)
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user
