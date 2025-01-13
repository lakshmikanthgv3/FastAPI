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
    prefix='/Phone_number',
    tags=['Phone Number Update'],
)

models.Base.metadata.create_all(bind=engine)

class UpdatePhoneNumber(BaseModel):
    Phone_number:str

def get_db():
    db = LocalSession()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

@router.get("")
async def get_details(db:db_dependency, user:user_dependency):
    model_data = db.query(users).filter(user.get('username') == users.username).all()
    if model_data is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='user is not authenticated')
    return model_data

@router.put("/update", status_code=status.HTTP_204_NO_CONTENT)
async def update_password(user:user_dependency,
                      db:db_dependency,
                      Phone_Update:UpdatePhoneNumber):
    user_details = db.query(users).filter(users.username == user.get('username')).first()
    if user_details is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='user is not authenticated')

    user_details.Phone_number = Phone_Update.Phone_number
    db.add(user_details)
    db.commit()

