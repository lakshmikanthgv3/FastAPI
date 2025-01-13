from .utils import *
from routers.admin import get_current_user, get_db

app.dependency_overrides[get_db] = overrides_get_db
app.dependency_overrides[get_current_user]= overrides_get_current_user

def test_get_user_details(get_exam):
    response = client.get("/admin/exam")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [{'title':'python', 'description': 'python description', 'complete': False, 'priority': 5, 'id': 1, 'owner_id': 1}]


def test_delete_data(get_exam):
    response = client.delete("/admin/delete/1")
    assert response.status_code == status.HTTP_204_NO_CONTENT

    db = TEST_LOCAL_SESSION()
    model = db.query(exam).filter(exam.id == 1).first()
    assert model is None

def test_delete_data_not_found(get_exam):
    response = client.delete("/admin/delete/999")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {'detail': 'user is not authenticated'}
