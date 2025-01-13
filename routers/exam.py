from fastapi import APIRouter, Depends, HTTPException, status, Path, Request
import models as models
from database import Base, engine, LocalSession
from typing import Annotated
from sqlalchemy.orm import Session
from models import exam
from pydantic import BaseModel, Field
from .auth import get_current_user
from starlette.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

router = APIRouter(
    prefix='/exam',
    tags=['Exams']
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


templates = Jinja2Templates(directory="templates")

def redirect_to_login():
    redirect_response = RedirectResponse(url='/auth/login-page', status_code=status.HTTP_302_FOUND)
    redirect_response.delete_cookie(key='access_token')
    return redirect_response

@router.get("/edit-exam-page/{get_id}")
async def render_exam_edit_page(request:Request, get_id:int, db:db_dependency):
    try:
        user = get_current_user(request.cookies.get('access_token'))
        if user is None:
            return redirect_to_login()

        exams = db.query(exam).filter(exam.id == get_id).first()
        return templates.TemplateResponse('edit-exam.html', {'request':request, 'exams':exams, 'user':user})
    except:
        return redirect_to_login()

@router.get("/add-exam-page")
async def render_add_exam_page(request:Request):
    try:
        user = get_current_user(request.cookies.get('access_token'))
        if user is None:
            return redirect_to_login()

        return templates.TemplateResponse('add-exam.html', {'request':request, 'user':user})
    except:
        return redirect_to_login()

@router.get('/exam-page')
async def render_exam_page(request: Request, db:db_dependency):
    try:
        # return redirect_to_login()
        user = get_current_user(request.cookies.get("access_token"))
        # return {"user details are: ": "user"}
        if user is None:
            redirect_to_login()

        exams = db.query(exam).filter(exam.owner_id == user.get("id")).all()
        return templates.TemplateResponse("exam.html", {"request":request, "exams":exams, "user":user})
    except:
        redirect_to_login()


class UserDetailModel(BaseModel):
    title:str
    description:str
    priority:int = Field(gt=0, lt=6)
    complete:bool

@router.get("/read_all", status_code=status.HTTP_200_OK)
async def read_all(user:user_dependency,
                   db:db_dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='user is not authenticated')
    return db.query(exam).filter(user.get('id') == exam.owner_id).all()

@router.get("/specificData/{get_id}", status_code=status.HTTP_200_OK)
async def get_specific_data(user:user_dependency,
                            db:db_dependency,
                            get_id:int):
    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='user is not authenticated')
    user_details = db.query(exam).filter(exam.id == get_id).filter(exam.owner_id == user.get('id')).first()
    if user_details is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Data not found')
    return user_details

@router.post("/add_data", status_code=status.HTTP_201_CREATED)
async def add_new_data(user:user_dependency,
                       db:db_dependency,
                       userDetails:UserDetailModel):
    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='user is not authenticated')
    user_data_model = exam(**userDetails.model_dump(), owner_id=user.get('id'))
    db.add(user_data_model)
    db.commit()

@router.put("/update/{get_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_data(user:user_dependency,
                      db:db_dependency,
                      userDetails:UserDetailModel,
                      get_id:int=Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='user is not authenticated')
    db_data = db.query(exam).filter(exam.id == get_id).filter(exam.owner_id == user.get('id')).first()
    if db_data is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Data not found')

    db_data.title = userDetails.title
    db_data.description = userDetails.description
    db_data.priority = userDetails.priority
    db_data.complete = userDetails.complete

    db.add(db_data)
    db.commit()

@router.delete("/delete/{get_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_data(user:user_dependency,
                      db:db_dependency,
                      get_id:int):
    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='user is not authenticated')
    user_data = db.query(exam).filter(exam.id==get_id).filter(exam.owner_id == user.get('id')).first()
    if user_data is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Data not found')
    db.query(exam).filter(exam.id==get_id).filter(exam.owner_id == user.get('id')).delete()
    db.commit()
