from fastapi import HTTPException, status
from sqlalchemy.orm import Session
import schemas
import models
import auth


# Helper function to check if the current user is an admin
def is_admin(user: models.User) -> bool:
   return user.is_admin

# Registration 
def create_user(user: schemas.UserCreate, db: Session, current_user: models.User = None) -> models.User:
    """Create a new user."""
    if current_user and not is_admin(current_user):
        # Ensure only admin can create other admins
        user.is_admin = False  # Make sure regular users are never admin
    
    # Check if user already exists
    db_user = db.query(models.User).filter(
        models.User.username == user.username,
        models.User.email == user.email
    ).first()
    if db_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username or email already exists")
    
    hashed_password = auth.get_password_hash(user.password)

    new_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        first_name=user.first_name,
        last_name=user.last_name,
        address=user.address,
        phone_number=user.phone_number,
        is_admin=user.is_admin  # Admin status controlled by logic above
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# Login
def get_user(username: str, password: str, db: Session) -> schemas.Token:
    """Get user by username and verify password"""
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    if not auth.verify_password(password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password")
    
    # Prepare data for the token
    data = {"sub": username, "is_admin": user.is_admin}

    # Create the access token
    access_token = auth.create_access_token(data)

    # Return the token using the Token schema
    return schemas.Token(access_token=access_token, token_type="bearer")