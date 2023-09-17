import logging

from fastapi import FastAPI
from mongoengine import connect

from fastapi.middleware.cors import CORSMiddleware

from app.api.tweets.tweets import tweets_router
from app.api.users.user_authentication import authentication_router
from core.utils.constants import (
    MONGO_DB_HOST,
    MONGO_DB_PASSWORD,
    MONGO_DB_USERNAME,
)

logging.basicConfig(level=logging.DEBUG)

connect(
    host=MONGO_DB_HOST,
    port=27017,
    username=MONGO_DB_USERNAME,
    password=MONGO_DB_PASSWORD,
    db="tweets",
)

app = FastAPI()

app.include_router(authentication_router)
app.include_router(tweets_router)

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
