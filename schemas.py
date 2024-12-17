from pydantic import BaseModel, EmailStr
from datetime import date, datetime
from typing import Optional, List
from enum import Enum


class BookBase(BaseModel):
    title: str
    price: float
    publication_date: date
    description: Optional[str] = None

    class Config:  
        orm_mode = True


class BookCreate(BookBase):
    author_id : int
    category_ids: List[int]


class BookUpdate(BookBase):
    title: Optional[str]
    price: Optional[float] 
    publication_date: Optional[date]


class BookResponse(BookBase):
    pass


class AuthorCreate(BaseModel):
    first_name: str
    last_name: str
    biography: str

    class Config:  
        orm_mode = True


class AuthorUpdate(AuthorCreate):
    first_name: Optional[str]
    last_name: Optional[str]
    biography: Optional[str]


class AuthorResponse(AuthorCreate):
    id: int

   
class CategoryCreate(BaseModel):
    name: str

    class Config:
        orm_mode = True 


class CategoryUpdate(CategoryCreate):
    name: Optional[str]


class CategoryResponse(CategoryCreate):
    id: int


class UserBase(BaseModel):
    username: str
    email: EmailStr
    first_name: str
    last_name: str
    address: str
    phone_number: str
    # date_joined: datetime
    is_admin: Optional[bool] = False


class UserCreate(UserBase):
    password: str


class UserUpdate(UserBase):
    password: Optional[str] = None


class UserResponse(UserBase):
    pass

    class Config:
        orm_mode = True


class OrderEnum(str, Enum):
    PENDING = "pending"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


class OrderItemCreate(BaseModel):
    order_id: int
    book_id: int
    quantity: int
    price_at_time: float


class OrderCreate(BaseModel):
    user_id: int
    # order_date: Optional[datetime] = datetime.utcnow() # Optional, defaults to current time if not provided
    total_amount: float
    status: OrderEnum
    order_items: List[OrderItemCreate]


class OrderResponse(BaseModel):
    id: int
    user_id: int 
    order_date: datetime
    total_amount: float
    status: OrderEnum
    order_items: List[OrderItemCreate] = []


    class Config:
        orm_mode = True


class ReviewCreate(BaseModel):
    user_id: int
    book_id: int
    rating: int
    review_text: str
    # review_date: Optional[date] = date.today()


class ReviewResponse(ReviewCreate):
    id: int

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None