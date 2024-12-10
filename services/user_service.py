from fastapi import HTTPException, status
from sqlalchemy.orm import Session
import schemas
import models
import auth


# Registration
def create_user(user: schemas.UserCreate, db: Session) -> models.User:
    """Create a new user"""
    db_user = db.query(models.User).filter(
        models.User.username == user.username,
        models.User.email == user.email
        ).first()
    if db_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username already exists")
    hashed_password = auth.get_password_hash(user.password)
    new_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        first_name=user.first_name,
        last_name=user.last_name,
        address=user.address,
        phone_number=user.phone_number,
        date_joined=user.date_joined
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# Login
def get_user(username: str, password: str, db: Session) -> models.User:
    """Get user by username and verify password"""
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    if not auth.verify_password(password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password")
    return user