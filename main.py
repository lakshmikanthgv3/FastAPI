from fastapi import FastAPI, Depends, HTTPException, status, Path, Request
import models as models
from database import Base, engine, LocalSession
from typing import Annotated
from sqlalchemy.orm import Session
from models import exam
from pydantic import BaseModel, Field
from routers import exam, auth, admin, password, phone_number
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def test(request:Request):
    return RedirectResponse(url='/auth/login-page', status_code=status.HTTP_302_FOUND)


@app.get("/healthy", status_code = status.HTTP_200_OK)
async def get_healthy():
    return {'status':'Healthy'}


app.include_router(auth.router)
app.include_router(exam.router)
app.include_router(admin.router)
app.include_router(password.router)
app.include_router(phone_number.router)