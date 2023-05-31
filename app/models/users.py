from mongoengine import DateField, Document, StringField


class User(Document):
    email = StringField()
    username = StringField()
    name = StringField()
    dob = DateField()
    password = StringField()
