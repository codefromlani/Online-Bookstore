from fastapi import HTTPException, status
from sqlalchemy.orm import Session
import models
import schemas
 

def create_order(order: schemas.OrderCreate, db: Session) -> models.Order:

    user = db.query(models.User).filter(models.User.id == order.user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="User not found"
        )
    
    db_order = models.Order(
        user_id=order.user_id,
        status=order.status.value,
        total_amount=0
    )

    db.add(db_order)
    db.flush()

    # Create order items
    total_amount = 0
    order_items = []

    for item in order.order_items:
        book = db.query(models.Book).filter(models.Book.id == item.book_id).first()
        if not book:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail=f"Book with id {item.book_id} not found"
            )
        
        # Create order item
        db_order_item = models.OrderItem(
            order_id=db_order.id,
            book_id=item.book_id,
            quantity=item.quantity,
            price_at_time=book.price
        )

        order_items.append(db_order_item)
        total_amount += item.quantity * book.price

    db_order.total_amount = total_amount

    db.add_all(order_items)
    db.commit()
    db.refresh(db_order)
    return db_order

def get_order_with_items(order_id: int, db: Session) -> models.Order:
    
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    
    # Accessing the related order items directly via relationship
    order_items = order.order_items  # This uses the 'order_items' relationship

    order_response = schemas.OrderResponse(
        id=order.id,
        user_id=order.user_id,
        order_date=order.order_date,
        total_amount=order.total_amount,
        status=order.status,
        order_items=[schemas.OrderItemCreate(
            order_id=item.order_id,
            book_id=item.book_id,
            quantity=item.quantity,
            price_at_time=item.price_at_time
        ) for item in order_items]  # Convert each order item to its Pydantic model
    )

    return order_response

def update_order(order_id: int, order_data: schemas.OrderCreate, db: Session) -> models.Order:

    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    if order_data.status:
        order.status = order_data.status

    total_amount = 0
    # existing_item_ids = [item.book_id for item in order_data.order_items]
    # for item in order.order_items:
    #     if item.book_id not in existing_item_ids:
    #         db.delete()
    if order_data.order_items:
        order_items = []
        for item in order_data.order_items:
            book = db.query(models.Book).filter(models.Book.id == item.book_id).first()
            if not book:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Book with id {item.book_id} not found"
                )
            
            existing_item = db.query(models.OrderItem).filter(
                models.OrderItem.order_id == order_id,
                models.OrderItem.book_id == item.book_id
            ).first()
            if existing_item:
               existing_item.quantity = item.quantity
               existing_item.price_at_time = item.price_at_time
            else:
                db_order_item = models.OrderItem(
                    order_id=order.id,
                    book_id=item.book_id,
                    quantity=item.quantity,
                    price_at_time=book.price
                )

                order_items.append(db_order_item)
                
            total_amount += item.quantity * book.price
        
        order.total_amount = total_amount

        if order_items:
            db.add_all(order_items)

    db.commit()
    db.refresh(order)
    return order

def delete_order(order_id: int, book_id: int, db: Session) -> None:
    
    db_order_item = db.query(models.OrderItem).filter(
        models.OrderItem.order_id == order_id,
        models.OrderItem.book_id == book_id
    ).first()

    if not db_order_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order item not found"
        )
    db.delete(db_order_item)
    db.commit()

    return{"detail": "Order item deleted successfully"}