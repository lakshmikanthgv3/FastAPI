from .utils import *
from routers.phone_number import get_current_user, get_db

app.dependency_overrides[get_db] = overrides_get_db
app.dependency_overrides[get_current_user] = overrides_get_current_user

def test_phone_number_change(test_users):
    response = client.put("/Phone_number/update", json={"Phone_number":"8431096000"})
    assert response.status_code == status.HTTP_204_NO_CONTENT