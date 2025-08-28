from fastapi import Request, HTTPException, Depends, status
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
    auth = request.headers.get("Authorization")
    if not auth:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing token")

    if not auth.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token format")

    try:
        token = auth[7:]
        payload = verify_token(token)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=f"Invalid or expired token :{str(e)}")
    username = payload.get("username")
    user_id = payload.get("sub")

    if user_id:
        user = db.query(User).filter(User.id == int(user_id)).first()
    elif username:
        user = db.query(User).filter(User.username == username).first()
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Token payload missing subject")

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    return user
