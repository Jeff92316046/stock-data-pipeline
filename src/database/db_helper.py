import os
from sqlmodel import create_engine, Session
from sqlalchemy_utils import database_exists, create_database
from contextlib import contextmanager

from dotenv import load_dotenv


load_dotenv()
SERVER = os.getenv("POSTGRES_SERVER")
PORT = os.getenv("POSTGRES_PORT")
USERNAME = os.getenv("POSTGRES_USERNAME")
PASSWORD = os.getenv("POSTGRES_PASSWORD")
DB = os.getenv("POSTGRES_DB")

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