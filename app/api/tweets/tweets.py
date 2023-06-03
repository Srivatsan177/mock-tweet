from typing import Annotated

from fastapi import APIRouter, Header, Response, status

from lib.core.utils.auth import authentic_request,decode_jwt
from app.schemas.tweets import TweetCreateSchema, TweetSchema
from app.models.tweets import Tweet
from lib.core.utils.tweets.parsers import get_mentions_and_tags
import traceback

tweets_router = APIRouter(prefix="")


@tweets_router.get("/")
@authentic_request
def home(response: Response, authorization: Annotated[str | None, Header()] = None):
    return [ TweetSchema(id=str(tweet.id), username=tweet.username, tweet=tweet.tweet) for tweet in Tweet.objects().order_by("-_id")]

@tweets_router.post("/tweet")
@authentic_request
def create_tweet(tweet: TweetCreateSchema, response: Response, authorization: Annotated[str | None, Header()] = None):
    username=decode_jwt(authorization)["username"]
    tags,mentions = get_mentions_and_tags(tweet.tweet)
    tweet = Tweet(username=username, tweet=tweet.tweet, tags=tags, mentions=mentions)
    tweet.save()
    return { "id": str(tweet.id) }

@tweets_router.post("/comment-tweet/{tweet_id}")
@authentic_request
def comment_tweet(tweet: TweetCreateSchema,tweet_id: str,response: Response, authorization: Annotated[str | None, Header()] = None):
    try:
        tweet = Tweet.objects.get(id=tweet_id)
    except Tweet.DoesNotExist:
        # print(traceback.format_exc())
        response.status_code = status.HTTP_404_NOT_FOUND
        return { "msg": "tweet not found" }
    print(tweet.tweet)
    return "tweet_comment"