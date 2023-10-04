from .base_class import Base
import sqlalchemy


class FollowCount(Base):
    __tablename__ = "follow_count"
    user_id = sqlalchemy.Column(sqlalchemy.String(128), primary_key=True)
    following_count = sqlalchemy.Column(sqlalchemy.BIGINT(), default=0)
    follower_count = sqlalchemy.Column(sqlalchemy.BIGINT(), default=0)

