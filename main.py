from fastapi import FastAPI
from mongoengine import *
from mongoengine import connect
import os
from app.models.users import User
from dotenv import load_dotenv
from app.api.users.user_authentication import authentication_router

connect(host="mongodb", port=27017, username="root", password="root", db="tweets")

app = FastAPI()

app.include_router(authentication_router)
