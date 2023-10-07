import typing
from typing import Optional

from pydantic import BaseModel


class UserSignupSchema(BaseModel):
    email: str
    username: str
    name: str
    password: str


class UserSigninSchema(BaseModel):
    username: Optional[str]
    password: str


class UserProfileSchema(BaseModel):
    username: str
    email: str
    name: str
    dob: Optional[str] = None
    followers: typing.Optional[typing.List[str]] = None
    following: typing.Optional[typing.List[str]] = None


class FollowUserSchema(BaseModel):
    username: str
