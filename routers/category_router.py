from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from services import category_service
from database import get_db
from typing import List
import schemas
import models
import auth


router = APIRouter(
    tags=["Category"]
)

@router.post("/category/", response_model=schemas.CategoryResponse)
def create_category(
    category: schemas.CategoryCreate, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.admin_required)
    ):
    return category_service.create_category(category=category, db=db)

@router.get("/category/", response_model=List[schemas.CategoryResponse])
def get_categories(
    skip: int = 0, limit: int = 10, 
    db: Session = Depends(get_db)
    ):
    return category_service.get_categories(skip=skip, limit=limit, db=db)

@router.patch("/category/{category_id}", response_model=schemas.CategoryResponse)
def update_category(
    category_id: int, 
    updated_category: schemas.CategoryUpdate, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.admin_required)
    ):
    return category_service.update_category(category_id=category_id, updated_category=updated_category, db=db)

@router.delete("/category/{category_id}", response_model=None)
def delete_category(
    category_id: int, 
    db: Session = Depends(get_db),
    current_user: Session = Depends(auth.admin_required)
    ):
    return category_service.delete_category(category_id=category_id, db=db)