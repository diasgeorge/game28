from fastapi import APIRouter, Depends, HTTPException
import app
from app import schemas
from app import utils
from app import models
from fastapi import Depends, FastAPI, HTTPException, status
from app.database import get_db
from sqlalchemy.orm import Session
 

router = APIRouter(
     prefix="/game",
     tags=['game']
)

@router.get("/{id}",response_model=schemas.Gametable)
def get_user(id: int, db: Session = Depends(get_db)):
    game = db.query(models.Gameroom).filter(models.Gameroom.id == id).first()
    if not game:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"No Game Room with id: {id} was found")
    return game

@router.get("/{id}/start/", status_code=status.HTTP_201_CREATED,response_model=schemas.GameScoreDisplay)
def create_game(id: int, db: Session = Depends(get_db)):

    # Check if all Players in the table
    check_player1 = db.query(models.Gameroom).filter(models.Gameroom.id == id,models.Gameroom.player1 != None).first()
    
    if not check_player1:
        print(check_player1)
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Invalid Operation")
    
    check_all_players = db.query(models.Gameroom).filter(models.Gameroom.id == id,models.Gameroom.player1 != None, models.Gameroom.player2 != None, models.Gameroom.player3 != None, models.Gameroom.player4 != None ).first()
    
    if not check_all_players:
        print(check_all_players)
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Invalid Operation")
    
    #Start the Scores Table
    first_game = {"roundnumber" : "1","ateamscore" : "0","bteamscore" : "0","room_id": id}
    check_first_game = db.query(models.Scores).filter(models.Scores.room_id == id,models.Scores.roundnumber == 1).first()
    print(check_first_game)
    if check_first_game:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,detail=f"Invalid Operation")
    gamescore = schemas.GameScore(**first_game)
    new_gamescore = models.Scores(**gamescore.model_dump())
    db.add(new_gamescore)
    db.commit()
    db.refresh(new_gamescore)
    return new_gamescore

@router.get("/{id}/update/", status_code=status.HTTP_201_CREATED,response_model=schemas.GameScoreDisplay)
def create_game(id: int, db: Session = Depends(get_db)):

    # Check if all Players in the table
    check_player1 = db.query(models.Gameroom).filter(models.Gameroom.id == id,models.Gameroom.player1 != None).first()
    
    if not check_player1:
        print(check_player1)
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Invalid Operation")
    
    check_all_players = db.query(models.Gameroom).filter(models.Gameroom.id == id,models.Gameroom.player1 != None, models.Gameroom.player2 != None, models.Gameroom.player3 != None, models.Gameroom.player4 != None ).first()
    
    if not check_all_players:
        print(check_all_players)
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Invalid Operation")
    
    #Start the Scores Table
    first_game = {"roundnumber" : "1","ateamscore" : "0","bteamscore" : "0","room_id": id}
    check_first_game = db.query(models.Scores).filter(models.Scores.room_id == id,models.Scores.roundnumber == 1).first()
    print(check_first_game)
    if check_first_game:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,detail=f"Invalid Operation")
    gamescore = schemas.GameScore(**first_game)
    new_gamescore = models.Scores(**gamescore.model_dump())
    db.add(new_gamescore)
    db.commit()
    db.refresh(new_gamescore)
    return new_gamescore

@router.get("/{id}/restart/", status_code=status.HTTP_201_CREATED)
def create_game(id: int, db: Session = Depends(get_db)):

    # Check if all Players in the table
    check_player1 = db.query(models.Gameroom).filter(models.Gameroom.id == id,models.Gameroom.player1 != None).first()
    
    if not check_player1:
        print(check_player1)
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Invalid Operation")

    return {"Game": "ReStart"}
