from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import or_
import app
from app import schemas
from app import models,oauth2
from fastapi import Depends, HTTPException, status, Response
from app.database import get_db
from sqlalchemy.orm import Session,aliased
from sqlalchemy.sql import text

router = APIRouter(
    prefix="/tables",
    tags=['tables']
)

def gen_main_query(db):
    # Create aliased tables for player2, player3, and player4
    player2 = aliased(models.Users)
    player3 = aliased(models.Users)
    player4 = aliased(models.Users)
    query = db.query(
    models.Gameroom.id,
    models.Gameroom.room_name,
    models.Users.username.label('player1'),
    player2.username.label('player2'),
    player3.username.label('player3'),
    player4.username.label('player4')
    ).select_from(models.Gameroom).join(
        models.Users, models.Gameroom.player1 == models.Users.id  # Join for player1
    ).outerjoin(
        player2, models.Gameroom.player2 == player2.id  # Left join for player2
    ).outerjoin(
        player3, models.Gameroom.player3 == player3.id  # Left join for player3
    ).outerjoin(
        player4, models.Gameroom.player4 == player4.id  # Left join for player4
    )

    return query

@router.get("/",response_model=List[schemas.Gametable])
def get_gametables(db: Session = Depends(get_db),current_user : int = Depends(oauth2.get_current_user),limit:int = 10,search: Optional[str] = ""):
    query = gen_main_query(db)
    # Execute the query and fetch results
    results = query.filter(models.Gameroom.room_name.contains(search)).limit(limit).all()
    print(results)
    return results

@router.post("/", status_code=status.HTTP_201_CREATED,response_model=schemas.CreatedGametable)
def create_gametable(gametables: schemas.CreateGameRoom, db: Session = Depends(get_db),current_user : int = Depends(oauth2.get_current_user)):
    if current_user is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"You Dont Have permissions to do this")
    gametables.player1 = current_user.id
    new_gametable = models.Gameroom(**gametables.model_dump())
    db.add(new_gametable)
    db.commit()
    db.refresh(new_gametable)
    return new_gametable

@router.get("/{id}",response_model=schemas.Gametable)
def get_gametables(id: int, db: Session = Depends(get_db),current_user : int = Depends(oauth2.get_current_user)):
    query = gen_main_query(db)
    gametable = query.filter(models.Gameroom.id == id).first()
    if not gametable:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"No Game Room with id: {id} was found")
    return gametable

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_gametables(id: int, db: Session = Depends(get_db),current_user : int = Depends(oauth2.get_current_user)):
    gametable = db.query(models.Gameroom).filter(models.Gameroom.id == id,models.Gameroom.player1 == current_user.id)
    if not gametable.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"No Game Room with id: {id} was found")
    gametable.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}",response_model=schemas.Gametable)
def update_gametables(id: int, gamePlayers: schemas.UpdateGameRoom, db: Session = Depends(get_db),current_user : int = Depends(oauth2.get_current_user) ):
    query = gen_main_query(db)
    gametable = db.query(models.Gameroom).filter(models.Gameroom.id == id, models.Gameroom.player1 != current_user.id)
    if not gametable.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"No Game Room with id: {id} was found")
    
    gametable_player = db.query(models.Gameroom)
    gametable_player = gametable_player.filter(models.Gameroom.id == id)
    if gamePlayers.players == "player1":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"You Dont Have permissions to do this")
    elif gamePlayers.players == "player2":
        which_player = models.Gameroom.player2
        player_dict = {"player2" : current_user.id}
        game_player_all = gametable_player.filter(or_(models.Gameroom.player3 == current_user.id,models.Gameroom.player4 == current_user.id))
    elif gamePlayers.players == "player3":
        which_player = models.Gameroom.player3
        player_dict = {"player3" : current_user.id}
        game_player_all = gametable_player.filter(or_(models.Gameroom.player2 == current_user.id,models.Gameroom.player4 == current_user.id))
    elif gamePlayers.players == "player4":
        which_player = models.Gameroom.player4
        player_dict = {"player4" : current_user.id}
        game_player_all = gametable_player.filter(or_(models.Gameroom.player2 == current_user.id,models.Gameroom.player3 == current_user.id))

    #check if player is already present
    gametable_player1 = gametable_player.filter(or_(which_player.is_(None),which_player == current_user.id)).first()
    if not gametable_player1:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,detail=f"Game Room with id: {id} and player already is in use")
    if game_player_all.first():
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,detail=f"Game Room with id: {id} and player already is in use")
    gametable.update(player_dict,synchronize_session=False)
    db.commit()
    new_gametable = query.filter(models.Gameroom.id == id).first()
    return new_gametable