from sqlalchemy.orm import Session, aliased
from app import schemas
from app import utils
from app import models

def get_lead_player(id: int,db):
    # Create aliased tables for player2, player3, and player4
    player2 = aliased(models.Users)
    player3 = aliased(models.Users)
    player4 = aliased(models.Users)
    lead_player = db.query(
    models.Gameroom.lead_player,
    ).select_from(models.Gameroom).join(
        models.Users, models.Gameroom.player1 == models.Users.id  # Join for player1
    ).outerjoin(
        player2, models.Gameroom.player2 == player2.id  # Left join for player2
    ).outerjoin(
        player3, models.Gameroom.player3 == player3.id  # Left join for player3
    ).outerjoin(
        player4, models.Gameroom.player4 == player4.id  # Left join for player4
    ).filter(models.Gameroom.id == id).first()
    
    return lead_player[0]

def game_main_query(db):
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

def Check_if_game_in_progress(id:int, db):
    query = db.query(models.Scores).filter(models.Scores.room_id == id).first()
    return query