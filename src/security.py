from passlib.hash import bcrypt
from jose import JWTError, jwt
from datetime import datetime, timedelta
from .config import SECRET_KEY


def verify_password(plain_password, hashed_password):
    return bcrypt.verify(plain_password, hashed_password)

def get_password_hash(password):
    return bcrypt.hash(password)

def decode_data(data):
    try:
        payload = jwt.decode(data, SECRET_KEY, algorithms=["HS256"])
        return payload
    except JWTError:
        return None

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm="HS256")
    return encoded_jwt
