Online Bookstore

This is an online bookstore application built with FastAPI and SQLAlchemy.

Features
- CRUD operations for Books, Authors, Categories, Order and Reviews.
- User authentication.
- Many-to-many relationship between books and categories.
- Ability to add, update, delete, and view books, order for books and leave reviews.
 
Installation

To get started with this project, follow these steps:

- Clone the repository:
    git clone https://github.com/codefromlani/online-bookstore.git

- Navigate into the project directory:
    cd online-bookstore

- Create and activate a virtual environment:
  On Windows:
    python -m venv venv
    venv\Scripts\activate
  On macOS/Linux:
    python3 -m venv venv
    source venv/bin/activate

- Install dependencies:
    pip install -r requirements.txt

- To start the application, use:
    uvicorn main:app --reload
    This will start the FastAPI server locally at http://127.0.0.1:8000.

Endpoints

Books
GET /books/ – Get a list of books.
POST /books/ – Add a new book.
PATCH /books/{book_id} – Update a book by ID.
DELETE /books/{book_id} – Delete a book by ID.

Authors
GET /author/ – Get a list of authors.
POST /author/ – Add a new author.
PATCH /author/{author_id} – Update an author by ID.
DELETE /author/{author_id} – Delete an author by ID.

Category
GET /category/ – Get a list of categories.
POST /category/ – Add a new category.
PATCH /category/{category_id} – Update a category by ID.
DELETE /category/{category_id} – Delete a category by ID.

Users
POST /register/ – Create a new user account.
POST /login/ – Log in to an existing account.

Orders
GET /orders/ – Get a list of orders.
POST /orders/ – Create a new order.
PATCH /orders/{order_id} – Update an order by ID.
DELETE /orders/{order_id} – Delete an order by ID.

Reviews
GET /reviews/ – Get a list of reviews.
POST /reviews/ – Add a new review.