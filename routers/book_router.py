from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from services import book_service
import schemas
import models
import auth


router = APIRouter(
    tags=["Book"]
)

@router.post("/books/", response_model=schemas.BookResponse)
def create_book(
    book: schemas.BookCreate,
    db: Session = Depends(get_db),
    current: models.User = Depends(auth.admin_required)
):
    return book_service.create_book(book=book, db=db)

@router.get("/books/", response_model=schemas.BookResponse)
def get_books(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    return book_service.get_books(db=db, skip=skip, limit=limit)

@router.patch("/books/{book_id}", response_model=schemas.BookResponse)
def update_book(
    book_id: int,
    updated_book: schemas.BookUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.admin_required)
):
    return book_service.update_book(book_id=book_id, updated_book=updated_book, db=db)

@router.delete("/books/{book_id}", response_model=None)
def delete_book(
    book_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.admin_required)
):
    return book_service.delete_book(book_id=book_id, db=db)