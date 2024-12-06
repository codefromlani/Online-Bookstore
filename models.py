from sqlalchemy import Column, Integer, String, Text, ForeignKey, Float, Date, Enum
from database import Base
import enum
from datetime import datetime, date
from sqlalchemy.orm import relationship


class Author(Base):
    __tablename__ = "authors"
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    biography = Column(Text)

    books = relationship("Book", back_populates="author")

    def __repr__(self):
        return f"<Author(id={self.id}, first_name{self.first_name}, last_name{self.last_name})>"

class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)

    # Many-to-many relationship with Book via BookCategory junction table
    books = relationship("Book", secondary="book_categories", back_populates="categories")


class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True, index=True)
    author_id = Column(Integer, ForeignKey("authors.id"))
    category_id = Column(Integer, ForeignKey("categories.id"))
    title = Column(String, nullable=False,index=True)
    price = Column(Float, nullable=False)
    publication_date = Column(Date, nullable=False)
    description = Column(Text)

    author = relationship("Author", back_populates="books")
    # Many-to-many relation via BookCategory
    categories = relationship("Category", secondary="book_categories", back_populates="books")  
    reviews = relationship("Review", back_populates="book")
    order_items = relationship("OrderItem", back_populates="book")


class BookCategory(Base): #Junction table
    __tablename__ = "book_categories"
    book_id = Column(Integer, ForeignKey("books.id"))
    category_id = Column(Integer, ForeignKey("categories.id"))

    category = relationship("Category", back_populates="books")
    book = relationship("Book", back_populates="categories")


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
    date_joined = Column(datetime, default=datetime.utcnow)

    orders = relationship("Order", back_populates="user")
    reviews = relationship("Review", back_populates="user")


class OrderEnum(enum.Enum):
    PENDING = "pending"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    order_date = Column(datetime, default=datetime.utcnow)
    total_amount = Column(Float, nullable=False)
    status = Column(Enum(OrderEnum), nullable=False, index=True)

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
    book = relationship("Book", back_populates="order_items")

class Review(Base):
    __tablename__ = "reviews"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    book_id = Column(Integer, ForeignKey("books.id"))
    rating = Column(Integer)
    review_text = Column(String)
    review_date = Column(Date, default=date.today)

    book = relationship("Book", back_populates="reviews")
    user = relationship("User", back_populates="reviews")
