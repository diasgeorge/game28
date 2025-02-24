from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone

from sqlalchemy import and_
from app import models, schemas
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session,aliased
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


def get_current_active_users_in_game(id: int, db) -> list[models.Users]:

    # Retrieve list of players
    
    """Retrieves a list of currently logged in users from the database."""
    player1 = aliased(models.Users)
    player2 = aliased(models.Users)
    player3 = aliased(models.Users)
    player4 = aliased(models.Users)

    query = db.query(
    player1.username.label("player1"),
    player2.username.label("player2"),
    player3.username.label("player3"),
    player4.username.label("player4")
    ).select_from(models.Gameroom).join( player1, and_(models.Gameroom.player1 == player1.id, player1.is_active == True)
    ).outerjoin(player2, and_(models.Gameroom.player2 == player2.id, player2.is_active == True)
    ).outerjoin(player3, and_(models.Gameroom.player3 == player3.id, player3.is_active == True)
    ).outerjoin(player4, and_(models.Gameroom.player4 == player4.id, player4.is_active == True)
    )

    users = query.filter(models.Gameroom.id == id).all()  

    return users
