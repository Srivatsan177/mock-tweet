from mongoengine import Document, StringField, ListField, ObjectIdField

class Tweet(Document):
    username = StringField()
    tweet = StringField(max_length=512)
    tags = ListField()
    mentions = ListField()

    meta = { "allow_inheritance": True }

class TweetComment(Tweet):
    parent_tweet_id = ObjectIdField()
    comment: StringField(max_length=512)

    meta={
        "indexes": [
            "parent_tweet_id",
        ]
    }