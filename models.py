from sqlalchemy import Column, Integer, String, Text, ForeignKey, Float, Date, DateTime, Boolean
from database import Base
from enum import Enum
from datetime import datetime, date
from sqlalchemy.orm import relationship
from sqlalchemy import Enum as SQLAlchemyEnum

class Author(Base):
    __tablename__ = "authors"
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False, index=True)
    last_name = Column(String, nullable=False, index=True)
    biography = Column(Text)

    # One-to-many relationship with Book
    books = relationship("Book", back_populates="author")

    def __repr__(self):
        return f"<Author(id={self.id}, first_name={self.first_name}, last_name={self.last_name})>"

class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)

    # Many-to-many relationship with Book via BookCategory junction table
    # books = relationship("Book", secondary="book_categories", back_populates="categories")


class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True, index=True)
    author_id = Column(Integer, ForeignKey("authors.id"))
    # category_id = Column(Integer, ForeignKey("categories.id"))
    title = Column(String, nullable=False,index=True)
    price = Column(Float, nullable=False)
    publication_date = Column(Date, nullable=False)
    description = Column(Text)

    # One-to-many relationship with Author
    author = relationship("Author", back_populates="books")

    # Many-to-many relationship with Category via BookCategory
    # categories = relationship("Category", secondary="book_categories", back_populates="books")  

    # One-to-many relationship with Review
    reviews = relationship("Review", back_populates="book")

    # One-to-many relationship with OrderItem
    order_items = relationship("OrderItem", back_populates="book")


# Junction table for many-to-many relationship between Book and Category
class BookCategory(Base): #Junction table
    __tablename__ = "book_categories"
    book_id = Column(Integer, ForeignKey("books.id"), primary_key=True)
    category_id = Column(Integer, ForeignKey("categories.id"), primary_key=True)

     # Relationships to Category and Book
    # category = relationship("Category", back_populates="books")
    # book = relationship("Book", back_populates="categories")

    category = relationship("Category", backref="book_categories")
    book = relationship("Book", backref="book_categories")


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    address = Column(String)
    phone_number = Column(String)
    date_joined = Column(DateTime, default=datetime.utcnow)
    is_admin = Column(Boolean, default=False)

    # One-to-many relationship with Order
    orders = relationship("Order", back_populates="user")

    # One-to-many relationship with Review
    reviews = relationship("Review", back_populates="user")


# Enum for Order status
class OrderEnum(str, Enum):
    PENDING = "PENDING"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    order_date = Column(DateTime, default=datetime.utcnow)
    total_amount = Column(Float, nullable=False)
    status = Column(SQLAlchemyEnum(OrderEnum), nullable=False, index=True)

    # Many-to-one relationship with User
    user = relationship("User", back_populates="orders")

    # One-to-many relationship with OrderItem
    order_items = relationship("OrderItem", back_populates="order")


class OrderItem(Base):
    __tablename__ = "order_items"
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    book_id = Column(Integer, ForeignKey("books.id"))
    quantity = Column(Integer, nullable=False)
    price_at_time = Column(Float, nullable=False)

    # Many-to-one relationship with Order
    order = relationship("Order", back_populates="order_items")

    # Many-to-one relationship with Book
    book = relationship("Book", back_populates="order_items")

class Review(Base):
    __tablename__ = "reviews"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    book_id = Column(Integer, ForeignKey("books.id"))
    rating = Column(Integer)
    review_text = Column(String)
    review_date = Column(Date, default=date.today)

    # Many-to-one relationship with Book
    book = relationship("Book", back_populates="reviews")

     # Many-to-one relationship with User
    user = relationship("User", back_populates="reviews")
