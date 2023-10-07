import re
import typing

from fastapi import APIRouter, Response, Header, status
from core.utils.auth import authentic_request, decode_jwt
from typing import Annotated, List, Type
from core.models.users import User
from core.schemas.users import UserProfileSchema
from core.utils.tweets.rest_utils import get_pydantic_from_mongo
from pydantic import BaseModel

router = APIRouter(prefix="/user")


@router.get("")
@authentic_request
def get_user_profile(search_username: str = None, response: Response = None,
                     authorization: Annotated[str | None, Header()] = None) -> UserProfileSchema:
    username = decode_jwt(authorization)["username"] if search_username is None else search_username
    user = User.objects.get(username=username)
    user_profile = UserProfileSchema(
        username=user.username,
        email=user.email,
        name=user.name,
        followers=user.followers,
        following=user.following,
    )
    response.status_code = status.HTTP_200_OK
    return user_profile


@router.get("/list")
@authentic_request
def search_users(search_username: str = None, response: Response = None,
                 authorization: Annotated[str | None, Header()] = None) -> typing.List[UserProfileSchema]:
    pattern = re.compile(f".*{search_username}.*", re.IGNORECASE)
    users = User.objects(username=pattern)
    users = [get_pydantic_from_mongo(UserProfileSchema, user) for user in users]
    return users
