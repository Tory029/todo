from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, declarative_base


DATABASE_URL = "postgresql+psycopg2://todo:Dd7878789@localhost:5433/todo_db"
engine = create_engine(DATABASE_URL)
session_local = sessionmaker(bind=engine, autocommit=False, autoflush=False)
metadata = MetaData()


Base = declarative_base()

def init_db():
    Base.metadata.create_all(bind=engine)