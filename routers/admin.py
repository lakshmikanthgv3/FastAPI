from fastapi import APIRouter, Depends, HTTPException, status, Path
import models as models
from database import Base, engine, LocalSession
from typing import Annotated
from sqlalchemy.orm import Session
from models import exam
from pydantic import BaseModel, Field
from .auth import get_current_user

router = APIRouter(
    prefix='/admin',
    tags=['admin'],
)

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = LocalSession()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

@router.get("/exam", status_code=status.HTTP_200_OK)
async def get_details(db:db_dependency, user:user_dependency):
    if user is None or user.get('user_role') != 'admin':
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='user is not authenticated')
    return db.query(exam).all()

@router.delete("/delete/{get_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_data(user:user_dependency,
                      db:db_dependency,
                      get_id:int=Path(gt=0)):
    user_data = db.query(exam).filter(exam.id==get_id).first()

    if user_data is None or user.get('user_role') !='admin':
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='user is not authenticated')
    db.query(exam).filter(exam.id==get_id).delete()
    db.commit()

