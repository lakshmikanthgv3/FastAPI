from .utils import *
from routers.password import get_current_user, get_db

app.dependency_overrides[get_db] = overrides_get_db
app.dependency_overrides[get_current_user] = overrides_get_current_user

def test_user_details(test_users):
    response = client.get("/password_change/user")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['username'] == 'ganesh'
    assert response.json()['email'] == 'ganesh@gmail.com'
    assert response.json()['first_name'] == 'ganesh'
    assert response.json()['last_name'] == 'G V'
    assert response.json()['role'] == 'admin'
    assert response.json()['Phone_number'] == '8431096010'


def test_change_password(test_users):
    response = client.put("/password_change/update", json={'password': 'test12345', 'new_password':'newpassword'})
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_change_password_invalid_current_password(test_users):
    response = client.put("/password_change/update", json={'password': 'wrongpassword', 'new_password':'newpassword'})
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {'detail': 'user enters a wrong password'}


