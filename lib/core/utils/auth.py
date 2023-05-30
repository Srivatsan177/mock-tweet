from hashlib import sha256
from .constants import PASSWORD_HASH_KEY, AUTHENTICATION_HASH_KEY
import hmac
import jwt
import datetime
import json

AUTH_EXPIRE_TIME = 8*60*60

def hash_data(data: str) -> str:
    return hmac.new(PASSWORD_HASH_KEY.encode(), data.encode(), sha256).hexdigest()

def get_jwt(data_dict: dict) -> str:
    data_dict["exp"] = datetime.datetime.now() + datetime.timedelta(AUTH_EXPIRE_TIME)
    print(data_dict, AUTHENTICATION_HASH_KEY)
    return jwt.encode(data_dict, AUTHENTICATION_HASH_KEY, "HS256")
