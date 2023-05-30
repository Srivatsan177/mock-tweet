import os
from mongoengine import Document, StringField, DateField


class User(Document):
    email = StringField()
    username = StringField()
    name = StringField()
    dob = DateField()
    password = StringField()
