from .utils import *
from routers.auth import authenticate_user_data, get_db, create_access_token, ALGORITHM, SECRET_KEY, get_current_user
from jose import jwt
from datetime import timedelta
import pytest
from fastapi import HTTPException

app.dependency_overrides[get_db] = overrides_get_db

def test_authenticate_user_data(test_users):
    db = TEST_LOCAL_SESSION()

    authenticated_user = authenticate_user_data(test_users.username, 'test12345', db)
    assert authenticated_user is not None
    assert authenticated_user.username == test_users.username

    non_existent_user = authenticate_user_data('wrongusername', 'test12345', db)
    assert non_existent_user is False

    password_incorrect = authenticate_user_data(test_users.username, 'wrongpassword', db)
    assert password_incorrect is False

def test_create_access_token():
    username = 'testuser'
    user_id = 1
    user_role = 'user'
    expires_delta = timedelta(days=1)

    token = create_access_token(username, user_role, user_id, expires_delta)

    user_details = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM],
                              options={'verify_signature':False})
    assert user_details['sub'] == username
    assert user_details['id'] == user_id
    assert user_details['role'] == user_role

@pytest.mark.asyncio
async def test_get_current_user_valid_token():
    user = {'sub':'testuser', 'id':1, 'role':'admin'}
    token = jwt.encode(user, SECRET_KEY, algorithm=ALGORITHM)

    current_user = get_current_user(token=token)
    assert current_user == {'username':'testuser', 'id':1, 'user_role':'admin'}


@pytest.mark.asyncio
async def test_get_current_user_missing_payload():
    encode = {'role':'user'}
    token = jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

    with pytest.raises(HTTPException) as Exceptinfo:
        await get_current_user(token=token)

    assert Exceptinfo.value.status_code == status.HTTP_400_BAD_REQUEST
    assert Exceptinfo.value.detail == 'user is not authenticated'

