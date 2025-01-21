import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker,DeclarativeMeta
from sqlalchemy_utils import database_exists, create_database

from dotenv import load_dotenv


load_dotenv()
SERVER = os.getenv("SERVER")
PORT = os.getenv("PORT")
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")
DB = os.getenv("DB")

engine_url = f"postgresql://{USERNAME}:{PASSWORD}@{SERVER}:{PORT}/{DB}"
engine = create_engine(
    engine_url,
    pool_pre_ping=True,
    pool_size=20,
    max_overflow=30,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(object):
    pass

Base = declarative_base(cls=Base)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def check_database_has_create():
    engine = create_engine(engine_url)
    if not database_exists(engine.url):
        create_database(engine.url)
