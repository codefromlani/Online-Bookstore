from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
import schemas
import models
import auth
from services import author_service


router = APIRouter(
    tags=["Author"]
)

@router.post("/author/", response_model=schemas.AuthorResponse)
def create_author(
    author: schemas.AuthorCreate, 
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(auth.admin_required)
    ):
    return author_service.create_author(author=author, db=db)

@router.get("/author/", response_model=schemas.AuthorResponse)
def get_authors(
    skip: int = 0, limit: int = 5, 
    db: Session = Depends(get_db)
    ):
    return author_service.get_authors(db=db, skip=skip, limit=limit)

@router.patch("/author/{author_id}", response_model=schemas.AuthorResponse)
def update_author(
    author_id: int, 
    updated_author: schemas.AuthorUpdate, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.admin_required)
    ):
    return author_service.update_author(author_id=author_id, updated_author=updated_author, db=db)

@router.delete("/author/{author_id}", response_model=None)
def delete_author(
    author_id: int, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.admin_required)
    ):
    return author_service.delete_author(author_id=author_id, db=db)