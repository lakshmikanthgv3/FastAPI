from fastapi import APIRouter, Depends, HTTPException, status, Path
import models as models
from database import Base, engine, LocalSession
from typing import Annotated
from sqlalchemy.orm import Session
from models import exam, users
from pydantic import BaseModel, Field
from .auth import get_current_user
from passlib.context import CryptContext

router = APIRouter(
    prefix='/password_change',
    tags=['password change'],
)

models.Base.metadata.create_all(bind=engine)

class updatePassword(BaseModel):
    password:str
    new_password:str

def get_db():
    db = LocalSession()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]
bcypt_context = CryptContext(schemes='bcrypt', deprecated='auto')

@router.get("/user", status_code=status.HTTP_200_OK)
async def get_details(db:db_dependency, user:user_dependency):
    model_data = db.query(users).filter(user.get('username') == users.username).first()
    if model_data is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='user is not authenticated')
    return model_data

@router.put("/update", status_code=status.HTTP_204_NO_CONTENT)
async def update_password(user:user_dependency,
                      db:db_dependency,
                      password_change:updatePassword):
    user_details = db.query(users).filter(users.username == user.get('username')).first()
    if user_details is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='user is not authenticated')
    if not bcypt_context.verify(password_change.password, user_details.hashed_password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='user enters a wrong password')

    user_details.hashed_password = bcypt_context.hash(password_change.new_password)
    db.add(user_details)
    db.commit()

