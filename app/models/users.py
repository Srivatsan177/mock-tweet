import os
from mongoengine import Document, connect, StringField, DateField

connect(host="localhost", port=27017, username="root", password="root", db="tweets")


class User(Document):
    email = StringField()
    username = StringField()
    name = StringField()
    dob = DateField()
    password = StringField()
