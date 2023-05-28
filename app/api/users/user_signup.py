from fastapi import APIRouter
from app.schemas.users import UserSignupSchema
import typing
import logging
from app.models.users import User

logging.basicConfig(level=logging.DEBUG)

signup_router = APIRouter(prefix="/users")


@signup_router.post("/signup", response_model=UserSignupSchema)
def signup(user: UserSignupSchema):
    user = User(**user.dict())
    logging.debug(user)
    return user
