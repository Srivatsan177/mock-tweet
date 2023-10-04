from core.pg_models.tweets import TweetLike
from core.pg_models.followers import FollowCount
from core.utils.db_util import DbHelper


def create_tweet_like(tweet_id: str) -> None:
    session = DbHelper().get_connection()
    with session.begin() as connection:
        tweet_like = TweetLike(tweet_id=tweet_id)
        connection.add(tweet_like)


def create_user_follower(user_id: str) -> None:
    session = DbHelper().get_connection()
    with session.begin() as connection:
        user_follower_count = FollowCount(user_id=user_id)
        connection.add(user_follower_count)
