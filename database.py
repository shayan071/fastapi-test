
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

#It manages communication between your application and DB.
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

#Whenever an API needs database access, we create a session from this factory.
SessionLocal = sessionmaker(
    autocommit=False, #since we are using sqlite
    autoflush=False,
    bind=engine
)

#Base = declarative_base()
"""
In SQLAlchemy, the declarative base is the foundational class used in
Object-Relational Mapping (ORM) to map Python classes directly to database
tables. It acts as a central registry that automatically links your
application's object structures with your relational database schema"""
class Base(DeclarativeBase):
    pass


"""
This is a FastAPI dependency, It:
1. Opens a database session.
2. Gives the session to the API endpoint.
3. Allows the endpoint to perform queries.
4. Closes the session after the request."""
def get_db():
    db = SessionLocal()
    try:
        yield db

    finally:
        db.close()

#now we define database tables in models.py that will use this database.py file