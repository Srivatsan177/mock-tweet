from pydantic import BaseModel
from typing import Optional


class TweetCreateSchema(BaseModel):
    tweet: str


class TweetSchema(BaseModel):
    id: str
    username: str
    tweet: str
    like: int
    liked_by_user: bool
    image_name: Optional[str] = None
