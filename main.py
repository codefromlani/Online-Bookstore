from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from database import get_db, Base, engine
from datetime import timedelta
from routers import author_router, category_router, user_router, book_router, order_router, review_router
import auth
import schemas


Base.metadata.create_all(bind=engine)

app = FastAPI(title="Online-Bookstore")



app.include_router(author_router.router)
app.include_router(category_router.router)
app.include_router(book_router.router)
app.include_router(user_router.router)
app.include_router(order_router.router)
app.include_router(review_router.router)

@app.get("/")
def home():
    return {"message": "Hello there! Welcome to my Online-Bookstore"}

@app.post("/token", response_model=schemas.Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """Login endpoint to get access token"""
    user = auth.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}