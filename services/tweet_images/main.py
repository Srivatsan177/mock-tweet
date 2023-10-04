from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.images import router as images_router
from core.utils.constants import (
    MONGO_DB_HOST,
    MONGO_DB_PASSWORD,
    MONGO_DB_USERNAME,
)
import logging
from mongoengine import connect

connect(
    host=MONGO_DB_HOST,
    port=27017,
    username=MONGO_DB_USERNAME,
    password=MONGO_DB_PASSWORD,
    db="tweets",
)

logging.basicConfig(level=logging.DEBUG)

app = FastAPI()

app.include_router(images_router)


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

