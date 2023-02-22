from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.main import app
from app.config import settings
from app.database import get_db, Base
from app.oath2 import create_access_token
from app import models
import pytest


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

# Create a test user for functions that you need to be logged in
@pytest.fixture()
def test_user(client):
    user_data = {
        "email" : "andrew@lemonmail.com",
        "password" : "ilikebread"
    }
    res = client.post("/users/", json=user_data)

    assert res.status_code == 201

    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user

# Create a test user for functions that you need to be logged in
@pytest.fixture()
def test_user_second(client):
    user_data = {
        "email" : "heyyymikey@lemonmail.com",
        "password" : "ilikeoranges"
    }
    res = client.post("/users/", json=user_data)

    assert res.status_code == 201

    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user

@pytest.fixture
def token(test_user):
    return create_access_token({"user_id" : test_user['id']})

@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization" : f"Bearer {token}"
    }
    return client

@pytest.fixture
def test_posts(test_user, db_session, test_user_second):
    posts_data = [
    {
        "title": "first title",
        "content": "first content",
        "owner_id": test_user['id']
    }, {
        "title": "2nd title",
        "content": "2nd content",
        "owner_id": test_user['id']
    },
        {
        "title": "3rd title",
        "content": "3rd content",
        "owner_id": test_user['id']
    }, {
        "title": "bleur title",
        "content": "lebleaux content",
        "owner_id": test_user_second['id']
    }]

    def create_post_model(post):
        return models.Post(**post)

    post_map = map(create_post_model, posts_data)
    posts = list(post_map)

    db_session.add_all(posts)

    db_session.commit()

    posts = db_session.query(models.Post).all()

    return posts
