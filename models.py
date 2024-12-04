from sqlalchemy import Column, Integer, String, Text, ForeignKey, Float, Date, Enum
from database import Base
import enum
from datetime import datetime
from sqlalchemy.orm import relationship


class Author(Base):
    __tablename__ = "authors"
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    biography = Column(Text)

    books = relationship("Book", back_populates="author")

class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)

    books = relationship("Book", back_populates="category")


class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True, index=True)
    author_id = Column(Integer, ForeignKey("authors.id"))
    category_id = Column(Integer, ForeignKey("categories.id"))
    title = Column(String)
    price = Column(Float)
    publication_date = Column(Date, nullable=False)
    description = Column(Text)

    author = relationship("Author", back_populates="books")
    category = relationship("Category", back_populates="books")


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    address = Column(String)
    phone_number = Column(String)
    date_joined = Column(datetime, default=datetime.utcnow)

    orders = relationship("Order", back_populates="user")


class OrderEnum(enum.Enum):
    PENDING = "pending"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    order_date = Column(datetime, default=datetime.utcnow)
    total_amount = Column(Float, nullable=False)
    status = Column(Enum(OrderEnum), nullable=False)

    user = relationship("User", back_populates="orders")
    order_items = relationship("OrderItem", back_populates="order")


class OrderItem(Base):
    __tablename__ = "order_items"
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    book_id = Column(Integer, ForeignKey("books.id"))
    quantity = Column(Integer, nullable=False)
    price_at_time = Column(Float, nullable=False)

    order = relationship("Order", back_populates="order_items")

class Review(Base):
    __tablename__ = "reviews"
    id = Column(Integer, primary_key=True, index=True)
    