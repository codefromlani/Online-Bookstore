# Categories are needed when creating or updating books, but categories 
# themselves have their own lifecycle (create, read, update, delete).


from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
import schemas
import models


def create_category(category: schemas.CategoryCreate, db: Session) -> models.Category:
    """Create a new book category/genie"""
    db_category = db.query(models.Category).filter(models.Category.name == category.name).first()
    if db_category:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"{category.name} category already exists")
    
    new_category = models.Category(name=category.name)
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category

def get_categories(db: Session, skip: int = 0, limit: int = 5) -> List[models.Category]:
    """Get a list of all categories"""
    return db.query(models.Category).offset(skip).limit(limit).all()

def get_category(category_id: int, db: Session) -> models.Category:
    """Get a category by ID"""
    db_category = db.query(models.Category).filter(models.Category.id == category_id).first()
    if db_category is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Category with ID {category_id} is not found")
    return db_category

def update_category(category_id: int, updated_category: schemas.CategoryUpdate, db: Session) -> Optional[models.Category]:
    """Update an existing category"""
    db_category = db.query(models.Category).filter(models.Category.id == category_id).first()
    if db_category is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Category with ID {category_id} is not found")
    
    if updated_category.name:
        db_category.name=updated_category.name

    db.commit()
    db.refresh(db_category)
    return db_category

def delete_category(category_id: int, db: Session) -> None:
    """Delete a category"""
    db_category = db.query(models.Category).filter(models.Category.id == category_id).first()
    if db_category is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Category with ID {category_id} is not found")
    db.delete(db_category)
    db.commit()