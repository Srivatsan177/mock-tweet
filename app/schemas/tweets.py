from pydantic import BaseModel

class TweetCreateSchema(BaseModel):
    tweet: str

class TweetSchema(BaseModel):
    id: str
    username: str
    tweet: str