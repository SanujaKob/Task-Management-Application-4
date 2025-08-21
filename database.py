# database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# SQLite DB file (created in the project folder)
SQLALCHEMY_DATABASE_URL = "sqlite:///./task_manager.db"

# For SQLite, this flag avoids thread errors with the dev server
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Session factory: used this in endpoints to talk to the DB
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for ORM models (tables will inherit from this)
Base = declarative_base()

# Dependency to get a DB session (FastAPI will open/close per request)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
