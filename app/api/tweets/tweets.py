from typing import Annotated

from fastapi import APIRouter, Header, Response, status

from lib.core.utils.auth import authentic_request, decode_jwt
from app.schemas.tweets import TweetCreateSchema, TweetSchema
from app.models.tweets import Tweet
from lib.core.utils.tweets.parsers import get_mentions_and_tags
from lib.core.utils.tweets.rest_utils import get_pydantic_from_mongo
import traceback
import logging

tweets_router = APIRouter(prefix="")


@tweets_router.get("/")
@authentic_request
def home(response: Response, authorization: Annotated[str | None, Header()] = None):
    return [
        TweetSchema(id=str(tweet.id), username=tweet.username, tweet=tweet.tweet)
        for tweet in Tweet.basic_tweet_objects().order_by("-_id")
    ]


@tweets_router.get("/tweet/{tweet_id}")
@authentic_request
def get_tweet(
    tweet_id: str,
    response: Response,
    authorization: Annotated[str | None, Header()] = None,
):
    try:
        tweet = Tweet.objects.get(id=tweet_id)
        tweet_comments = Tweet.objects(parent_tweet_id=tweet.id)
        return {
            "tweet": get_pydantic_from_mongo(TweetSchema, tweet),
            "tweet_comments": [
                get_pydantic_from_mongo(TweetSchema, x) for x in tweet_comments
            ],
        }

    except Tweet.DoesNotExist:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"msg": "Tweet not found"}
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        logging.debug(traceback.format_exc())
        return {"msg": "Internal Server Error"}


@tweets_router.post("/tweet")
@authentic_request
def create_tweet(
    tweet: TweetCreateSchema,
    response: Response,
    authorization: Annotated[str | None, Header()] = None,
):
    username = decode_jwt(authorization)["username"]
    tags, mentions = get_mentions_and_tags(tweet.tweet)
    tweet = Tweet(username=username, tweet=tweet.tweet, tags=tags, mentions=mentions, parent_tweet_id=None)
    tweet.save()
    return {"id": str(tweet.id)}


@tweets_router.post("/comment-tweet/{tweet_id}")
@authentic_request
def comment_tweet(
    tweet: TweetCreateSchema,
    tweet_id: str,
    response: Response,
    authorization: Annotated[str | None, Header()] = None,
):
    try:
        parent_tweet = Tweet.objects.get(id=tweet_id)
    except Tweet.DoesNotExist:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"msg": "tweet not found"}
    tags, mentions = get_mentions_and_tags(tweet.tweet)
    username = decode_jwt(authorization)["username"]
    comment_tweet = Tweet(
        parent_tweet_id=parent_tweet.id,
        tweet=tweet.tweet,
        tags=tags,
        mentions=mentions,
        username=username,
    ).save()
    return {"id": str(comment_tweet.id)}
