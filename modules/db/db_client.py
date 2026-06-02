from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from resources.db_creds import DBCreds

USERNAME = DBCreds.USERNAME
PASSWORD = DBCreds.PASSWORD
HOST = DBCreds.HOST
PORT = DBCreds.PORT
TABLE = DBCreds.TABLE

engine = create_engine(
    f"postgresql+psycopg2://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{TABLE}", echo=True
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db_session():
    """Создает новую сессию БД"""
    return SessionLocal()
