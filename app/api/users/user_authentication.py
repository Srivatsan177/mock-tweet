from fastapi import APIRouter, status, Response
from app.schemas.users import UserSignupSchema, UserSigninSchema
import typing
import logging
from app.models.users import User
from lib.core.utils.auth import hash_data, get_jwt
from mongoengine.errors import NotUniqueError
from app.schemas.messages import GenericResponse
import traceback

logging.basicConfig(level=logging.DEBUG)

authentication_router = APIRouter(prefix="/users")


@authentication_router.post("/signup", response_model=GenericResponse)
def signup(user: UserSignupSchema, response: Response):
    user.password = hash_data(user.password)
    try:
        user = User(**user.dict()).save()
    except NotUniqueError:
        response.status_code = status.HTTP_403_FORBIDDEN
        return GenericResponse(msg="Username or email already in use")
    except Exception as e:
        logging.error(traceback.format_exc())
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return GenericResponse(msg="Server Error")
    response.status_code = status.HTTP_201_CREATED
    return GenericResponse(msg="Successfully created account!!")

@authentication_router.post("/signin")
def signin(user_details: UserSigninSchema, response: Response):
    user = User.objects(username=user_details.username)[:1][0]
    if user.password == hash_data(user_details.password):
        response.status_code = status.HTTP_200_OK
        return { "jwt": get_jwt({ "user": user.username, "email": user.email }) }
    response.status_code = status.HTTP_404_NOT_FOUND
    return
