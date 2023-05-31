import os

# Used to hash user password
PASSWORD_HASH_KEY = os.environ.get("PASSWORD_HASH_KEY")

# Used by jwt encoder and decoder
AUTHENTICATION_HASH_KEY = os.environ["AUTHENTICATION_HASH_KEY"]

# MONGO Credentials
MONGO_DB_HOST = os.environ["MONGO_DB_HOST"]
MONGO_DB_USERNAMAE = os.environ["MONGO_DB_USERNAME"]
MONGO_DB_PASSWORD = os.environ["MONGO_DB_PASSWORD"]
