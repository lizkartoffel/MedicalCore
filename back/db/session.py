from sqlmodel import create_engine, Session

# Create a connection string for an SQLite database
sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

# Setup the engine (connect_args is needed for SQLite to handle concurrent requests safely)
engine = create_engine(sqlite_url, echo=True, connect_args={"check_same_thread": False})

def create_db_and_tables():
    """Initializes the database and creates all tables defined in models.py"""
    # Import all models before calling this, which is handled in main.py
    from models import SQLModel
    SQLModel.metadata.create_all(engine)

def get_session():
    """Dependency function to yield a new database session"""
    with Session(engine) as session:
        yield session

# from sqlmodel import SQLModel, create_engine, Session
# #from supabase import create_client, Client
# from core import config  

# engine = create_engine("sqlite:///database.db")

# def create_db_and_tables():
#     """Create all database tables"""
#     SQLModel.metadata.create_all(engine)

# def get_session():
#     with Session(engine) as session:
#         yield session

# supabase: Client = create_client(
#     supabase_url=config.SUPABASE_URL, 
#     supabase_key=config.SUPABASE_KEY
# )