from fastapi import FastAPI
from api.follow import router as follow_router
from fastapi.middleware.cors import CORSMiddleware
from mongoengine import connect
from core.utils.constants import MONGO_DB_HOST, MONGO_DB_PASSWORD, MONGO_DB_USERNAME

app = FastAPI()

app.include_router(follow_router)

connect(
    host=MONGO_DB_HOST,
    port=27017,
    username=MONGO_DB_USERNAME,
    password=MONGO_DB_PASSWORD,
    db="tweets",
)

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
