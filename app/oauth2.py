from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from app import models, schemas
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.config import settings
from app.database import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes


def create_access_token(data: dict):
    to_encode = data.copy()

    expire =datetime.now(timezone.utc).replace(tzinfo=None) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)

    return encoded_jwt


def verify_access_token(token : str, credentials_exception):

    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        id : str = payload.get("user_id")
        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=id)

    except JWTError:
        return credentials_exception
    
    return token_data 
    

def get_current_user(token : str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    
    credentials_exception  = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Could not Validate Credentials",headers={"WWW-Authenticate": "Bearer"})
    user_token = verify_access_token(token,credentials_exception)
    if isinstance(user_token, HTTPException):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Could not Validate Credentials",headers={"WWW-Authenticate": "Bearer"})
    user = db.query(models.Users).filter(models.Users.id == user_token.id).first()

    return user