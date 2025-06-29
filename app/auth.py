from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
from database import get_db
import models
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
import os
from dotenv import load_dotenv
OAuthScheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

load_dotenv()
EXPIRE_TOKEN_TIME = int(os.getenv("EXPIRE_TOKEN_TIME"))
KEY = os.getenv("KEY")
ALGORITHM = os.getenv("ALGORITHM")


def create_access_token(data: dict):
    encode_data = data.copy()
    expiry = datetime.utcnow() + timedelta(minutes=EXPIRE_TOKEN_TIME)
    encode_data.update({"exp": expiry})
    encoded_jwt = jwt.encode(encode_data, key=KEY, algorithm=ALGORITHM)  # string here
    return encoded_jwt

def verify_user(token: str = Depends(OAuthScheme), db: Session = Depends(get_db)):
    authentication_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        payload = jwt.decode(token, key=KEY, algorithms=[ALGORITHM])  # list
        email: str = payload.get("sub")
        if email is None:
            raise authentication_exception
        user = db.query(models.User).filter(models.User.email == email).first()
        if user is None:
            raise authentication_exception
        return {"id":user.id, "email":user.email}
    except JWTError:
        raise authentication_exception
