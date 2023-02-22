from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.main import app
from app.config import settings
from app.database import get_db, Base
import pytest

##### I'm Useless, all moved to conftest

########################################################################################
########################################################################################
#
# Setup test Database
#
########################################################################################

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

########################################################################################

# Rescope so that tests can run without creating new tables for every test, only
# For every time we run the whole test suite
# ^ Bad practice, all tests should be independent of one-another
@pytest.fixture(scope="function")
def db_session():
    # Drop all tables to start clean
    # Do it here instead of after yield that way if code stops we can see the tables
    Base.metadata.drop_all(bind=engine)
    # Create tables
    Base.metadata.create_all(bind=engine)
    # Create DB session
    db = TestingSessionLocal()
    try: 
        yield db
    finally:
        db.close()

@pytest.fixture(scope="function")
def client(db_session):
    def override_get_db():
        try: 
            yield db_session
        finally:
            db_session.close()

    app.dependency_overrides[get_db] = override_get_db
    # Yield gives flexibility to run code before the return
    yield TestClient(app)
    # and we can run stuff after
    