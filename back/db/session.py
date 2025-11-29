from sqlmodel import SQLModel, create_engine, Session
from supabase import create_client, Client
from core import config  

engine = create_engine("sqlite:///database.db")

def create_db_and_tables():
    """Create all database tables"""
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

supabase: Client = create_client(
    supabase_url=config.SUPABASE_URL, 
    supabase_key=config.SUPABASE_KEY
)