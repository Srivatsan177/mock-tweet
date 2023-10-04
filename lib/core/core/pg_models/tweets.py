from .base_class import Base
import sqlalchemy


class TweetLike(Base):
    __tablename__ = "tweet_like"
    tweet_id = sqlalchemy.Column(sqlalchemy.String, primary_key=True)
    like_count = sqlalchemy.Column(sqlalchemy.BIGINT, default=0)
