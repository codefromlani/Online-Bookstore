from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from services import review_service
from typing import List
import auth 
import models
import schemas


router = APIRouter(
    tags=["Review"]
)

@router.post("/reviews/", response_model=schemas.ReviewResponse)
def create_review(
    review: schemas.ReviewCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    return review_service.create_review(review=review, db=db)

@router.get("/reviews/{book_id}", response_model=List[schemas.ReviewResponse])
def get_reviews(
    book_id: int,
    db: Session = Depends(get_db)
):
    return review_service.get_reviews_for_book(book_id=book_id, db=db)