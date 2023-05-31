import logging

from fastapi import FastAPI
from mongoengine import connect

from app.api.tweets.tweets import tweets_router
from app.api.users.user_authentication import authentication_router
from lib.core.utils.constants import (
    MONGO_DB_HOST,
    MONGO_DB_PASSWORD,
    MONGO_DB_USERNAMAE,
)

logging.basicConfig(filename="app.log", level=logging.DEBUG)

connect(
    host=MONGO_DB_HOST,
    port=27017,
    username=MONGO_DB_USERNAMAE,
    password=MONGO_DB_PASSWORD,
    db="tweets",
)

app = FastAPI()

app.include_router(authentication_router)
app.include_router(tweets_router)
