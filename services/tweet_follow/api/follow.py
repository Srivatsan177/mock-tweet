from fastapi import APIRouter, Header, Response, status
from core.utils.auth import authentic_request, decode_jwt
from core.schemas.users import FollowUserSchema
from typing import Annotated
from core.models.users import User

router = APIRouter(prefix="/follow")


@router.get("")
@authentic_request
def follow(follow_username: str, response: Response,
           authorization: Annotated[str | None, Header()] = None):
    username = decode_jwt(authorization)["username"]
    user = User.objects.get(username=username)
    if follow_username not in user.following:
        user.following.append(follow_username)
        user.save()
    follow_user = User.objects.get(username=follow_username)
    if username not in follow_user.followers:
        follow_user.followers.append(username)
        follow_user.save()
    response.status_code = status.HTTP_200_OK
    return response


@router.get("/unfollow")
@authentic_request
def unfollow(unfollow_username: str, response: Response, authorization: Annotated[str | None, Header()] = None):
    username = decode_jwt(authorization)["username"]

    # Remove following from user
    User.objects(username=username).update_one(pull__following=unfollow_username)

    # Remove followers from unfollow_user
    User.objects(username=unfollow_username).update_one(pull__followers=username)
    response.status_code = status.HTTP_200_OK
    return response
