from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from services import user_service
from database import get_db
import auth
import schemas
import models


router = APIRouter(
    tags=["User"]
)

@router.post("/register/", response_model=schemas.UserResponse)
def create_user(
        user: schemas.UserCreate, 
        db: Session = Depends(get_db),
        # current_user: models.User = Depends(auth.admin_required)
):
    return user_service.create_user(user=user, db=db, current_user=None)

@router.post("/login/", response_model=schemas.Token)
def get_user(
    username: str,
    password: str,
    db: Session = Depends(get_db),
    
):
    user = user_service.get_user(username=username, password=password, db=db)
    return user