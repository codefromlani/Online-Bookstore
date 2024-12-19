from fastapi import HTTPException, status
from sqlalchemy.orm import Session
import models 
import schemas


def create_review(review: schemas.ReviewCreate, db: Session) -> models.Review:

    user = db.query(models.User).filter(models.User.id == review.user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    book = db.query(models.Book).filter(models.Book.id == review.book_id).first()
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found"
        )
    
    if review.rating < 1 or review.rating > 5:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Rating must be between 1 and 5"
        )
    
    db_review = models.Review(
        user_id=review.user_id,
        book_id=review.book_id,
        review_text=review.review_text,
        rating=review.rating 
    )

    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review

def get_reviews_for_book(book_id: int, db: Session) -> models.Review:
    reviews = db.query(models.Review).filter(models.Review.book_id == book_id).all()
    if not reviews:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No reviews found for this book"
        )
    return reviews

