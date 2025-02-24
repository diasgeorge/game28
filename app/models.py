import datetime
from typing import List
from typing import Optional
from sqlalchemy import DateTime, ForeignKey, Integer, String, Boolean 
from sqlalchemy.sql import func
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

class Base(DeclarativeBase):
    pass
class Users(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    username : Mapped[str] = mapped_column(String(30),nullable=False,unique=True)
    email : Mapped[str] = mapped_column(String(30),nullable=False,unique=True)
    password : Mapped[str] = mapped_column(String(90),nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    is_active: Mapped[bool] = mapped_column(Boolean,nullable=False,server_default="False")
    def __repr__(self) -> str:
        return f"Users(id={self.id!r}, email={self.email!r})"
    
class Gameroom(Base):
    __tablename__ = "gamerooms"
    id: Mapped[int] = mapped_column(primary_key=True)
    room_name: Mapped[str] = mapped_column(String(30),nullable=False)
    player1: Mapped[int] = mapped_column(ForeignKey("users.id",ondelete="CASCADE"))
    player2: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id"))
    player3: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id"))
    player4: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id"))
    lead_player:  Mapped[str] = mapped_column(nullable=False,default="player1",server_default="player1")
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    scores: Mapped[List["Scores"]] = relationship(
        back_populates="gamerooms", cascade="all, delete-orphan"
    )
    gameplayscores: Mapped[List["GamePlayScores"]] = relationship(
        back_populates="gamerooms", cascade="all, delete-orphan"
    )
    def __repr__(self) -> str:
        return f"Gameroom(id={self.id!r}, roomname={self.room_name!r}, hostedby={self.player1!r})"

class Scores(Base):
    __tablename__ = "scores"
    id: Mapped[int] = mapped_column(primary_key=True)
    roundnumber: Mapped[int] = mapped_column(nullable=False)
    ateamscore: Mapped[int] = mapped_column(nullable=False)
    bteamscore: Mapped[int] = mapped_column(nullable=False)
    room_id: Mapped[int] = mapped_column(Integer, ForeignKey('gamerooms.id'), unique=True, nullable=False)
    gamerooms: Mapped["Gameroom"] = relationship(back_populates="scores")
    gameplayscores: Mapped["GamePlayScores"] = relationship(back_populates="scores")
    def __repr__(self) -> str:
        return f"Scores(id={self.id!r}, roomid={self.room_id!r})"
    

class GamePlayScores(Base):
    __tablename__ = "gameplayscores"
    id: Mapped[int] = mapped_column(primary_key=True)
    player1_predict: Mapped[int] = mapped_column(nullable=False,default=0)
    player2_predict: Mapped[int] = mapped_column(nullable=False,default=0)
    player3_predict: Mapped[int] = mapped_column(nullable=False,default=0)
    player4_predict: Mapped[int] = mapped_column(nullable=False,default=0)
    round_winner: Mapped[str] = mapped_column(nullable=False)
    round_number : Mapped[int] = mapped_column(nullable=False,default=0)
    room_id: Mapped[int] = mapped_column(Integer, ForeignKey('gamerooms.id'),nullable=False)
    score_id: Mapped[int] = mapped_column(ForeignKey("scores.id"))
    gamerooms: Mapped["Gameroom"] = relationship(back_populates="gameplayscores")
    scores: Mapped["Scores"] = relationship(back_populates="gameplayscores")
    def __repr__(self) -> str:
        return f"GamePlayScores(id={self.id!r}, roomid={self.room_id!r})"
    


