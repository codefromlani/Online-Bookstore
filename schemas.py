from pydantic import BaseModel
from datetime import date
from typing import Optional


class BookBase(BaseModel):
    title: str
    price: float
    publication_date = date
    description: Optional[str] = None


class BookCreate(BookBase):
    author_id : int
    category_id: int


class BookUpdate(BookBase):
    title: Optional[str]
    price: Optional[float] 
    publication_date: Optional[date]