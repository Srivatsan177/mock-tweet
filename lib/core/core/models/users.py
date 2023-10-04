from mongoengine import DateField, Document, StringField, ListField


class User(Document):
    email = StringField()
    username = StringField()
    name = StringField()
    dob = DateField()
    password = StringField()
    followers = ListField()
    following = ListField()

    meta = {
        "indexes": [
            {
                "fields": ["username"],
                "unique": True,
            },
            {"fields": ["email"], "unique": True},
        ]
    }
