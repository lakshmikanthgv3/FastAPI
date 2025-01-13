from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
from fastapi.testclient import TestClient
from main import app
from fastapi import status
import pytest
from pytest import fixture
from models import exam, users
from routers.auth import bcypt_context

TEST_DATABASE_URL = 'sqlite:///./test.db'
engine = create_engine(TEST_DATABASE_URL)

TEST_LOCAL_SESSION = sessionmaker(bind=engine)
Base = declarative_base()

def overrides_get_db():
    db = TEST_LOCAL_SESSION()
    try:
        yield db
    finally:
        db.close()

def overrides_get_current_user():
    return {'username':'ganesh', 'id':1, 'user_role':'admin'}


client = TestClient(app)


@pytest.fixture
def get_exam():
    exams = exam(
        title="python",
        description ="python description",
        priority=5,
        complete=False,
        owner_id = 1
    )
    db = TEST_LOCAL_SESSION()
    db.add(exams)
    db.commit()
    yield exams
    with engine.connect() as connection:
        connection.execute(text("delete from exam"))
        connection.commit()


@pytest.fixture
def test_users():
    user = users(
        email='ganesh@gmail.com',
        username = 'ganesh',
        first_name = 'ganesh',
        last_name = 'G V',
        hashed_password = bcypt_context.hash('test12345'),
        role = 'admin',
        Phone_number = '8431096010'
    )
    db = TEST_LOCAL_SESSION()
    db.add(user)
    db.commit()
    yield user
    with engine.connect() as connection:
        connection.execute(text("delete from users"))
        connection.commit()