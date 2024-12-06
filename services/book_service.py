from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
import models
import schemas

def create_book(book: schemas.BookCreate, db: Session) -> models.Book:
    """Create a new book"""
    db_book = db.query(models.Book).filter(
        models.Book.title == book.title,
        models.Book.author_id == book.author_id
    ).first()
    if db_book:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="This author already has a book with the same title"
        )
    
    new_book = models.Book(
        title=book.title,
        price=book.price,
        publication_date=book.publication_date,
        description=book.description,
        author_id=book.author_id,
        category_id=book.category_id
    )
    db.add(new_book)
    db.commit()
    db.refresh(new_book)

    return new_book

def get_book(db: Session, skip: int = 0, limit: int = 10) -> List[models.Book]:
    """Retrieve books from the database"""
    db_book = db.query(models.Book).offset(skip).limit(limit).all()
    return db_book

def get_book_by_id(book_id: int, db: Session) -> models.Book:
    """Retrieve book by id"""
    db_book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if db_book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=(f"Book with the id {book_id} is not found")
        )
    return db_book

def update_book(book_id: int, updated_book: schemas.BookUpdate, db: Session) -> Optional[models.Book]:
    """Update a book"""
    db_book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if db_book is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=(f"Book with the id {book_id} is not found")
            )
    if updated_book.title:
         db_book.title=updated_book.title
    if updated_book.price:
         db_book.price=updated_book.price
    if updated_book.publication_date:
         db_book.publication_date=updated_book.publication_date
    if updated_book.description:
         db_book.description=updated_book.description

    db.commit()
    db.refresh(db_book)
    return db_book

def delete_book(book_id: int, db: Session) -> None:
    """Delete a book from the database"""
    db_book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if db_book is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=(f"Book with the id {book_id} is not found")
            )
    db.delete(db_book)
    db.commit()