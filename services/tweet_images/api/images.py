import logging
from typing import Annotated

from fastapi import APIRouter, Response, Header, status
from core.models.tweets import Tweet
from core.schemas.images import ImageInformationSchema
from core.utils.s3_util import get_s3_presigned_url
from core.utils.auth import authentic_request

router = APIRouter(prefix="/images")


@router.get("/get-s3-url/{tweet_id}")
@authentic_request
def get_s3_url(tweet_id: str, image_name: str, response: Response,
               authorization: Annotated[str | None, Header()] = None):
    try:
        tweet = Tweet.objects.get(id=tweet_id)
        if tweet.image_name is None:
            _, extension = image_name.split(".")
            s3_url = get_s3_presigned_url(f"images/{tweet.id}.{extension}", "put_object")
            tweet.image_name = f"images/{tweet.id}.{extension}"
            tweet.save()
        else:
            s3_url = get_s3_presigned_url(tweet.image_name, "get_object")
        return s3_url
    except Tweet.DoesNotExist:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"msg": "Tweet Not found"}
