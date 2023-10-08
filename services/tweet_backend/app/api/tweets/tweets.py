from typing import Annotated

import sqlalchemy
from fastapi import APIRouter, Header, Response, status

from core.utils.auth import authentic_request, decode_jwt
from core.schemas.tweets import TweetCreateSchema, TweetSchema
from core.models.tweets import Tweet, TweetLike
from core.models.users import User
from core.utils.tweets.parsers import get_mentions_and_tags
from core.utils.tweets.rest_utils import (
    get_pydantic_from_mongo,
    tweet_liked_by_user,
)
import traceback
import logging
from core.utils.kafka_util import get_kafka_producer
from core.dataclass_containers.tweets import TweetLike as TweetLikeContainer
from core.utils.constants import KAFKA_USER_LIKE_TOPIC
import json
from core.utils.create_pg_records import create_tweet_like
from core.pg_models.tweets import TweetLike as TweetLikePG
from core.utils.db_util import DbHelper

tweets_router = APIRouter(prefix="")

kafka_producer = get_kafka_producer()

@tweets_router.get("/")
@authentic_request
def home(response: Response, authorization: Annotated[str | None, Header()] = None):
    username = decode_jwt(authorization)["username"]
    session = DbHelper().get_connection()
    tweets = []
    with session.begin() as connection:
        tweets = [
            TweetSchema(
                id=str(tweet.id),
                username=tweet.username,
                tweet=tweet.tweet,
                like=connection.execute(
                    sqlalchemy.select(TweetLikePG).where(TweetLikePG.tweet_id == str(tweet.id))).first()[0].like_count,
                liked_by_user=tweet_liked_by_user(tweet.id, username),
                image_name=tweet.image_name
            )
            for tweet in Tweet.basic_tweet_objects().order_by("-_id")
        ]
    return tweets


@tweets_router.get("/tweet/{tweet_id}")
@authentic_request
def get_tweet(
        tweet_id: str,
        response: Response,
        authorization: Annotated[str | None, Header()] = None,
):
    try:
        username = decode_jwt(authorization)["username"]
        tweet = Tweet.objects.get(id=tweet_id)
        tweet_comments = Tweet.objects(parent_tweet_id=tweet.id)
        return {
            "tweet": get_pydantic_from_mongo(
                TweetSchema,
                tweet,
                custom_mappings={
                    "like": TweetLike.objects(tweet_id=tweet_id).count(),
                    "liked_by_user": tweet_liked_by_user(tweet_id, username)
                },
            ),
            "tweet_comments": [
                get_pydantic_from_mongo(TweetSchema, x, custom_mappings={
                    "like": TweetLike.objects(tweet_id=x.id).count(),
                    "liked_by_user": tweet_liked_by_user(x.id, username)
                }) for x in tweet_comments
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
    tweet = Tweet(
        username=username,
        tweet=tweet.tweet,
        tags=tags,
        mentions=mentions,
        parent_tweet_id=None,
    )
    tweet.save()
    create_tweet_like(tweet_id=str(tweet.id))
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
    create_tweet_like(tweet_id=str(comment_tweet.id))
    return {"id": str(comment_tweet.id)}


@tweets_router.post("/like-tweet/{tweet_id}")
@authentic_request
def like_tweet(
        tweet_id: str,
        response: Response,
        authorization: Annotated[str | None, Header()] = None,
):
    try:
        tweet = Tweet.objects.get(id=tweet_id)
        username = decode_jwt(authorization)["username"]
        user = User.objects.get(username=username)
        # delete like if already exists
        tweet_like = TweetLike.objects.get(user_id=user.id, tweet_id=tweet.id)
        tweet_like.delete()
        tweet_like_container = TweetLikeContainer(id=tweet_id, value=-1)
        kafka_producer.send(KAFKA_USER_LIKE_TOPIC, json.dumps(tweet_like_container.__dict__).encode("utf-8"))
        return False
    except Tweet.DoesNotExist:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"msg": "Tweet not found"}
    except TweetLike.DoesNotExist:
        # If like does not exist we insert row
        tweet_like = TweetLike(tweet_id=tweet.id, user_id=user.id)
        tweet_like_container = TweetLikeContainer(id=tweet_id, value=1)
        kafka_producer.send(KAFKA_USER_LIKE_TOPIC, json.dumps(tweet_like_container.__dict__).encode("utf-8"))
        tweet_like.save()
        return True
