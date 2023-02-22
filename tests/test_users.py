import pytest
from app import schemas
from jose import jwt
from app.config import settings

def test_root(client):
    res = client.get("/")
    # assert res.json().get('message') == "Welcome to my API!!!"
    assert res.status_code == 200

def test_creat_user(client):
    # Must use trailing slash or response code will be wrong
    res = client.post("/users/", json=
    {
        "email" : "andrew@lemonmail.com",
        "password" : "ilikeike"
    })
    # Use pydantic model to validate response
    new_user = schemas.UserOut(**res.json())
    assert res.status_code == 201

def test_login_user(client, test_user):
    # No trailing slash here bc there's no prefix. Make sure it matches the API
    # Change from json= to data= since login form isn't JSON
    res = client.post("/login", data=
    {
        "username" : test_user['email'],
        "password" : test_user['password']
    })
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(login_res.access_token, settings.secret_key, algorithms=[settings.algorithm])
    id = payload.get("user_id")
    assert id == test_user['id']
    assert login_res.token_type == "bearer"
    assert res.status_code == 200

@pytest.mark.parametrize("email, password, status_code", [
    ("wrongemail.com", "ilikebread", 403),
    ("andrew@lemonmail.com", "wrong_password", 403),
    ("wrongemail", "wrong_password", 403),
    (None, "ilikebread", 422),
    ("andrew@lemonmail.com", None, 422)
])
def test_bad_login(client, test_user, email, password, status_code):
    res = client.post("/login", data={
        "username" : email,
        "password" : password
    })
    assert res.status_code == status_code
    #assert res.json().get('detail') == "Invalid Cridentials"

    