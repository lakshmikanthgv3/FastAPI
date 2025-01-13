from .utils import *
from routers.exam import get_db, get_current_user

app.dependency_overrides[get_db] = overrides_get_db
app.dependency_overrides[get_current_user] = overrides_get_current_user

def test_healthy():
    response = client.get("/healthy")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'status':'Healthy'}

def test_read_all(get_exam):
    response = client.get("/exam/read_all")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [{'complete': False, 'description': 'python description',
                                'title': 'python', 'owner_id': 1, 'priority': 5, 'id': 1}]

def test_specific_data(get_exam):
    response = client.get("/exam/specificData/1")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'complete': False, 'description': 'python description',
                                'title': 'python', 'owner_id': 1, 'priority': 5, 'id': 1}

def test_specific_data_not_authenticated(get_exam):
    response = client.get("/exam/specificData/999")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {'detail': 'Data not found'}

def test_add_data(get_exam):
    create_request = {
        'title':'java',
        'description':'java description',
        'priority':5,
        'complete':False
    }

    response = client.post("/exam/add_data", json=create_request)
    assert response.status_code == status.HTTP_201_CREATED

    db = TEST_LOCAL_SESSION()
    model = db.query(exam).filter(exam.id == 2).first()
    assert model.title == create_request.get('title')
    assert model.description == create_request.get('description')
    assert model.priority == create_request.get('priority')
    assert model.complete == create_request.get('complete')


def test_update_data(get_exam):
    request_data = {
        'title':'python updated',
        'description':'python description updated',
        'complete':False,
        'priority': 4
    }

    response = client.put("/exam/update/1", json=request_data)
    assert response.status_code == status.HTTP_204_NO_CONTENT

    db = TEST_LOCAL_SESSION()
    model = db.query(exam).filter(exam.id == 1).first()
    assert model.title == 'python updated'

def test_update_data_not_found(get_exam):
    request_data = {
        'title':'python updated',
        'description':'python description updated',
        'complete':False,
        'priority': 4
    }

    response = client.put("/exam/update/999", json=request_data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {'detail':'Data not found'}

def test_delete_data(get_exam):
    response = client.delete("/exam/delete/1")
    assert response.status_code == status.HTTP_204_NO_CONTENT

    db = TEST_LOCAL_SESSION()
    model = db.query(exam).filter(exam.id == 1).first()
    assert model is None

def test_delete_data_not_found(get_exam):
    response = client.delete("/exam/delete/999")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {'detail': 'Data not found'}





