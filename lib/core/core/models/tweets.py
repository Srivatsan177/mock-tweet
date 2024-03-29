from mongoengine import (
    Document,
    StringField,
    ListField,
    ObjectIdField,
    queryset_manager,
)


class Tweet(Document):
    username = StringField()
    tweet = StringField(max_length=512)
    tags = ListField()
    mentions = ListField()
    parent_tweet_id = ObjectIdField()
    image_name = StringField()

    meta = {
        "allow_inheritance": True,
        "indexes": ["username", "parent_tweet_id"],
    }

    @queryset_manager
    def basic_tweet_objects(doc_cls, queryset):
        return queryset.filter(parent_tweet_id=None)

    @queryset_manager
    def objects(doc_cls, queryset):
        return queryset.order_by("-_id")


class TweetLike(Document):
    tweet_id = ObjectIdField()
    user_id = ObjectIdField()
    meta = {
        "allow_inheritance": True,
        "indexes": [{"fields": ["tweet_id", "user_id"], "unique": True}],
    }
