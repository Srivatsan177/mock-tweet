from pydantic import BaseModel
from typing import *
from hashlib import sha256


class UserSignupSchema(BaseModel):
    email: str
    username: str
    name: str
    password: str

class UserSigninSchema(BaseModel):
    username: Optional[str]
    password: str