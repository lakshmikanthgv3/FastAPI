from fastapi import APIRouter, Depends, HTTPException, status, Path, Request
import models as models
from database import Base, engine, LocalSession
from typing import Annotated
from sqlalchemy.orm import Session
from models import users
from pydantic import BaseModel, Field
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from datetime import timedelta, datetime
from jose import jwt, JWTError
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware

router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

models.Base.metadata.create_all(bind=engine)
bcypt_context = CryptContext(schemes='bcrypt', deprecated='auto')
auth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')

SECRET_KEY = '604f4b0bb91cbf5d981f3152a0b2223eceaf22f18df22d1e7511a835da818a20'
ALGORITHM = 'HS256'

def get_db():
    db = LocalSession()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

class CreateUserModel(BaseModel):
    email:str
    username:str
    first_name:str
    last_name:str
    hashed_password:str
    role:str
    Phone_number:str


templates = Jinja2Templates(directory="templates")

@router.get("/login-page")
def login_page(request:Request):
    return templates.TemplateResponse("login.html", {"request":request})

@router.get("/register-page")
def register_page(request:Request):
    return templates.TemplateResponse("register.html", {"request":request})


def authenticate_user_data(username:str, password:str, db):
    user_details = db.query(users).filter(users.username == username).first()
    if not user_details:
        return False
    if not bcypt_context.verify(password, user_details.hashed_password):
        return False
    return user_details

def create_access_token(username:str, role:str, user_id:int, timedelta):
    encode = {'sub':username, 'id':user_id, 'role':role}
    expiry = datetime.now() + timedelta
    encode.update({'exp':expiry})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(token:Annotated[str, Depends(auth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username:str = payload.get('sub')
        user_id:int = payload.get('id')
        user_role:str = payload.get('role')
        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='user is not authenticated')
        return {'username':username, 'id':user_id, 'user_role':user_role}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='user is not authenticated')


@router.post("/")
async def create_new_user(db:db_dependency,
                          user_create:CreateUserModel):
    user_data = users(
        email = user_create.email,
        username = user_create.username,
        first_name = user_create.first_name,
        last_name = user_create.last_name,
        hashed_password = bcypt_context.hash(user_create.hashed_password),
        is_active = True,
        role=user_create.role,
        Phone_number = user_create.Phone_number
    )
    db.add(user_data)
    db.commit()

@router.post("/token")
async def authenticate_user(db:db_dependency,
                            form_data:Annotated[OAuth2PasswordRequestForm, Depends()]):
    user_authenticate = authenticate_user_data(form_data.username, form_data.password, db)

    if user_authenticate is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='user is not authenticated')

    token = create_access_token(user_authenticate.username, user_authenticate.role, user_authenticate.id, timedelta(minutes=20))
    return {'access_token':token, 'access_type':'Bearer'}
