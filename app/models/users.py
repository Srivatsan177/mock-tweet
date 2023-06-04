from mongoengine import DateField, Document, StringField


class User(Document):
    email = StringField()
    username = StringField()
    name = StringField()
    dob = DateField()
    password = StringField()

    meta = {
        "indexes": [
            {
                "fields": ["username"],
                "unique": True,
            },
            {"fields": ["email"], "unique": True},
        ]
    }
