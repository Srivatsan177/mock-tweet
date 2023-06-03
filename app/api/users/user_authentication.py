import logging
import traceback

from fastapi import APIRouter, Response, status
from mongoengine.errors import NotUniqueError

from app.models.users import User
from app.schemas.messages import GenericResponse
from app.schemas.users import UserSigninSchema, UserSignupSchema
from lib.core.utils.auth import AuthenticationException, auth_user, hash_data

authentication_router = APIRouter(prefix="/users")


@authentication_router.post("/signup", response_model=GenericResponse)
async def signup(user: UserSignupSchema, response: Response):
    user.password = hash_data(user.password)
    try:
        user = User(**user.dict()).save()
    except NotUniqueError:
        response.status_code = status.HTTP_403_FORBIDDEN
        return GenericResponse(msg="Username or email already in use")
    except Exception:
        logging.error(traceback.format_exc())
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return GenericResponse(msg="Server Error")
    response.status_code = status.HTTP_201_CREATED
    return GenericResponse(msg="Successfully created account!!")


@authentication_router.post("/signin")
async def signin(user_details: UserSigninSchema, response: Response):
    try:
        return auth_user(user_details)
    except AuthenticationException as e:
        response.status_code = status.HTTP_403_FORBIDDEN
        return {"msg": str(e)}
    except Exception:
        logging.error(traceback.format_exc())
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"msg": "Internal Server"}
