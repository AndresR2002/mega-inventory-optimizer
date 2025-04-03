from dotenv import load_dotenv
from sqlmodel import create_engine, Session, SQLModel
import os
load_dotenv()

db_url = os.getenv("DATABASE_URL")
engine = create_engine(db_url)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
