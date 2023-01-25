from jose import jwt, JWTError
from datetime import datetime, timedelta
from . import schemas, database, models
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .config import settings

oath2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Need 3 things:
# ------------------------
# SECRET KEY
# Algorithm - HS256
# Expiration time

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE = settings.access_token_expire_minutes

def create_access_token(data: dict):
    # Can play around with JWT tokens at jwt.io
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE)
    to_encode.update({"exp" : expire})

    jwt_token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return jwt_token

def verify_access_token(token: str, cridential_exception):

    try: 
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        id: str = payload.get("user_id")

        if not id:
            raise cridential_exception

        token_data = schemas.TokenData(id=id)

    except JWTError:
        raise cridential_exception

    return token_data

def get_current_user(token: str = Depends(oath2_scheme), db : Session = Depends(database.get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
        detail="could not validate credentials", headers={"WWW-Authenticate" : "Bearer"})
    
    token = verify_access_token(token, credentials_exception)

    user = db.query(models.User).filter(models.User.id == token.id).first()

    return user
    

