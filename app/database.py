from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config import settings

SQLALCHEMY_DATABASE_URL = f'postgresql+psycopg://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}' 

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)

sessionLocal = sessionmaker(autocommit=False, autoflush=True, bind=engine)

# declarative base class
class Base(DeclarativeBase):
    pass


def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()