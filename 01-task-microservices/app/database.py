from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .configs import DatabaseSettings

# Initialize settings
db_settings = DatabaseSettings.from_env()

# Create engine
engine = create_engine(db_settings.database_url(), echo=True)

# Create session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base
Base = declarative_base()


# Get DB function
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
