from fastapi import APIRouter, Depends, HTTPException
import app
from app import schemas
from app import utils
from app import models
from fastapi import Depends, FastAPI, HTTPException, status
from app.database import get_db
from sqlalchemy.orm import Session
 

router = APIRouter(
     prefix="/users",
     tags=['users']
)


@router.post("/", status_code=status.HTTP_201_CREATED,response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    #hash the password - user.password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    check_user = db.query(models.Users).filter(models.Users.email == user.email).first()

    if check_user:
        raise HTTPException(status_code=status.HTTP_302_FOUND,detail=f"User will email id : {user.email} already exists")
    
    check_username = db.query(models.Users).filter(models.Users.username == user.username).first()

    if check_username:
        raise HTTPException(status_code=status.HTTP_302_FOUND,detail=f"User name already exists")
    
    new_user = models.Users(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/{id}",response_model=schemas.UserResponse)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.Users).filter(models.Users.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"No user with id: {id} was found")
    return user