from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional
import models
import schemas


def create_author(author: schemas.AuthorCreate, db: Session) -> models.Author:
    """Creates a new author in the database if not already exists."""
    db_author = db.query(models.Author).filter(
        models.Author.first_name == author.first_name,
        models.Author.last_name == author.last_name
        ).first()
    if db_author:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An author with the same name already exists"
        )
    new_author = models.Author(
        first_name=author.first_name,
        last_name=author.last_name,
        biography=author.biography
    )
    db.add(new_author)
    db.commit()
    db.refresh(new_author)
    return new_author

def get_author_by_id(author_id: int, db: Session) -> models.Author:
    """Get an author by ID from the database"""
    db_author = db.query(models.Author).filter(models.Author.id == author_id).first()
    if db_author is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Author with ID {author_id} not found")
    return db_author

def update_author(author_id: int, updated_author: schemas.AuthorUpdate, db: Session) -> Optional[models.Author]:
    """Update an existing author's details"""
    db_author = db.query(models.Author).filter(models.Author.id == author_id).first()
    if db_author is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Author with ID {author_id} not found")
    
    if updated_author.first_name:
        db_author.first_name=updated_author.first_name
    if updated_author.last_name:
        db_author.last_name=updated_author.last_name
    if updated_author.biography:
        db_author.biography=updated_author.biography

    db.commit()
    db.refresh(db_author)
    return db_author

def delete_author(author_id: int, db: Session) -> None:
    """Delete an author from the database"""
    db_author = db.query(models.Author).filter(models.Author.id == author_id).first()
    if db_author is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Author with ID {author_id} not found")
    
    db.delete(db_author)
    db.commit()
    return {"detail": f"Author with ID {author_id} has been successfully deleted."}
