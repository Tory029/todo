from sqlalchemy import create_engine#, MetaData
from sqlalchemy.orm import sessionmaker, declarative_base
from db_config import settings


DATABASE_URL = settings.DATABASE_URL
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


Base = declarative_base()

def init_db():
    Base.metadata.create_all(bind=engine)


def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()