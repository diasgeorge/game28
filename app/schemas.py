from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr


class GameRoom(BaseModel):
    room_name: str
    player1: int
    player2: Optional[int] = None
    player3: Optional[int] = None
    player4: Optional[int] = None

class GameRoomBase(BaseModel):
    room_name: str
    player1: Optional[int] = None

class CreateGameRoom(GameRoomBase):
    pass

class UpdateGameRoom(BaseModel):
    players: str

class players(BaseModel):
    players: dict[str, int]


class Gametable(GameRoomBase):
    id: int
    room_name: str
    player1: str
    player2: Optional[str] 
    player3: Optional[str] 
    player4: Optional[str]

    class Config:
        from_attributes = True

class UserCreate(BaseModel):
    email : EmailStr
    username : str
    password : str


class UserResponse(BaseModel):
    id: int
    email : EmailStr
    username : str

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token : str
    token_type : str

class TokenData(BaseModel):
    id: Optional[int] = None


class GameScore(BaseModel):
    roundnumber: int
    ateamscore: int
    bteamscore: int
    room_id: int

class GameScoreDisplay(GameScore):
    pass