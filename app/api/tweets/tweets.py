from typing import Annotated

from fastapi import APIRouter, Header, Response

from lib.core.utils.auth import authentic_request

tweets_router = APIRouter(prefix="")


@tweets_router.get("/")
@authentic_request
def home(response: Response, authorization: Annotated[str | None, Header()] = None):
    return {"welcome": "home"}
