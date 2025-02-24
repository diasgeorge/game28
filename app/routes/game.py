from fastapi import APIRouter, Depends, HTTPException
from app import schemas,models,oauth2,game_utils
from fastapi import Depends, HTTPException, status
from app.database import get_db
from sqlalchemy.orm import Session

 

router = APIRouter(
     prefix="/game",
     tags=['game']
)



@router.get("/{id}",response_model=schemas.Gametable)
def get_user(id: int, db: Session = Depends(get_db)):
    
    query = game_utils.game_main_query(db)
    # Execute the query and fetch results
    game = query.filter(models.Gameroom.id == id).first()
    if not game:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"No Game Room with id: {id} was found")
    return game

@router.get("/{id}/start/", status_code=status.HTTP_201_CREATED,response_model=schemas.GameScoreDisplay)
def create_game(id: int, db: Session = Depends(get_db),current_user : int = Depends(oauth2.get_current_user)):

    lead_player = game_utils.get_lead_player(id,db)
    if (lead_player == "player1"):
        which_player = models.Gameroom.player1
    elif (lead_player == "player2"):
        which_player = models.Gameroom.player2
    elif (lead_player == "player3"):
        which_player = models.Gameroom.player3
    elif (lead_player == "player4"):
        which_player = models.Gameroom.player4
    # Check if all Players in the table
    check_lead_player = db.query(models.Gameroom).filter(models.Gameroom.id == id,which_player == current_user.id).first()
    if not check_lead_player:
        print(check_lead_player)
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Invalid Operation")
    
    active_users = oauth2.get_current_active_users_in_game(id,db)
    if len(*active_users) != 4:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Exactly four users must be logged in")
    
    
    #Check if Scores table is populated else Start the Scores Table
    game_progress = game_utils.Check_if_game_in_progress(id,db)
    if game_progress:
        round_number = game_progress.roundnumber + 1
        score_id = game_progress.id
        # Update the game progress with the new round number
        game_progress.roundnumber = round_number 
        db.commit()
        return game_progress
    else:
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

