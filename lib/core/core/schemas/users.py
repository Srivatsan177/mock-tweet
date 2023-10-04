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

class FollowUserSchema(BaseModel):
    username: str
