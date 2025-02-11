import os
from sqlmodel import create_engine, Session
from sqlalchemy_utils import database_exists, create_database
from contextlib import contextmanager

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

@contextmanager
def get_db():
    session = Session(engine)
    try:
        yield session
    finally:
        session.close()

def check_database_has_create():
    if not database_exists(engine.url):
        create_database(engine.url)
check_database_has_create()