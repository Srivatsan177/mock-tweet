from fastapi import FastAPI
from mongoengine import *
from mongoengine import connect
import os
from app.models.users import User
from dotenv import load_dotenv
from app.api.users.user_signup import signup_router

app = FastAPI()

app.include_router(signup_router)

