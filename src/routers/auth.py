from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.db_utils import get_db_session
from src.models import  User
from src.security import get_password_hash, verify_password, create_access_token
from fastapi.security import OAuth2PasswordRequestForm
from redis import Redis
from src.config import REDIS_URL
from datetime import timedelta
from src.schemas import UserCreate
from src.security import decode_data

router = APIRouter(prefix="/auth", tags=["auth"])

redis = Redis.from_url(REDIS_URL)


def get_user_id(token: str):
    data = redis.get(token)
    if data is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return decode_data(token)
    

@router.post("/register")
def register_user(user:UserCreate, db: Session = Depends(get_db_session)):
    hashed_password = get_password_hash(user.password)
    db_user = User(username=user.username, email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {"User successfully created."}

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db_session)):
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    
    access_token = create_access_token(data={"username": user.username, "isadmin":user.is_admin})
    redis.setex(access_token, timedelta(minutes=15), user.id)
    return {"access_token": access_token, "token_type": "bearer"}
