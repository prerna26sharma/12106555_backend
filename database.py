from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLite URL for the database
SQLALCHEMY_DATABASE_URL = "sqlite:///./tasks.db"

# Create the database engine
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

# Define a session for handling connections
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for ORM models
Base = declarative_base()

# Dependency function for the DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
