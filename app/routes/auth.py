from typing import List
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
import app
from app import schemas
from app import models
from fastapi import Depends, HTTPException, status, Response
from app import utils
from app import oauth2
from app.database import get_db
from sqlalchemy.orm import Session

router = APIRouter(
    tags=['Authentication']
)

@router.post("/login",response_model=schemas.Token)
def login(user_creds: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):

    user = db.query(models.Users).filter(models.Users.username == user_creds.username)
    user_data = user.first()
    if not user_data:
        raise HTTPException(status_3code=status.HTTP_403_FORBIDDEN,detail=f"Invalid Credentials")

    if not utils.verify(user_creds.password, user_data.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Invalid Credentials")
    
    #create a token and return token
    access_token = oauth2.create_access_token(data= {"user_id" : user_data.id})

    user.update({models.Users.is_active: True},synchronize_session='fetch')
    db.commit()

    return {"access_token" : access_token,
            "token_type" : "bearer" }