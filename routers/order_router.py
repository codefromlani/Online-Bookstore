from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from services import order_service
import auth 
import models
import schemas


router = APIRouter(
    tags=["Order"]
)

@router.post("/orders/", response_model=schemas.OrderResponse)
def create_order(
    order: schemas.OrderCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    return order_service.create_order(order=order, db=db)

@router.get("/orders/{order_id}", response_model=schemas.OrderResponse)
def get_orders(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    return order_service.get_order_with_items(order_id=order_id, db=db)

@router.patch("/orders/", response_model=schemas.OrderResponse)
def update_order(
    order_id: int,
    order_data: schemas.OrderCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    return order_service.update_order(order_id=order_id, order_data=order_data, db=db)

@router.delete("/orders/", response_model=None)
def delete_order(
    order_id: int,
    book_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    return order_service.delete_order(order_id=order_id, book_id=book_id, db=db)