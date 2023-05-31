import datetime
import hmac
import logging
from functools import wraps
from hashlib import sha256

import jwt
from fastapi import Response, status

from app.models.users import User

from .constants import AUTHENTICATION_HASH_KEY, PASSWORD_HASH_KEY

AUTH_EXPIRE_TIME = 8 * 60 * 60


class AuthenticationException(Exception):
    pass


def authentic_request(func):
    @wraps(func)
    def wrapper(*args, authorization: str, response: Response, **kwargs):
        try:
            logging.debug(authorization)
            if jwt.decode(authorization, AUTHENTICATION_HASH_KEY, "HS256"):
                return func(*args, authorization, **kwargs)

        except jwt.ExpiredSignatureError:
            response.status_code = status.HTTP_403_FORBIDDEN
            return {"msg": "session expired please login again"}
        except jwt.DecodeError:
            response.status_code = status.HTTP_403_FORBIDDEN
            return {"msg": "Login error please login again"}
        except Exception as e:
            logging.error(e)
            response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            return {"msg": "Internal Server Error"}

    return wrapper


def hash_data(data: str) -> str:
    return hmac.new(PASSWORD_HASH_KEY.encode(), data.encode(), sha256).hexdigest()


def get_jwt(data_dict: dict) -> str:
    data_dict["exp"] = datetime.datetime.now() + datetime.timedelta(AUTH_EXPIRE_TIME)
    return jwt.encode(data_dict, AUTHENTICATION_HASH_KEY, "HS256")


def auth_user(user_details):
    user = User.objects(username=user_details.username)[:1]
    if len(user) < 1:
        raise AuthenticationException("Account Not Found")
    user = user[0]
    if user.password != hash_data(user_details.password):
        raise AuthenticationException("Incorrect Password")
    else:
        return {"jwt": get_jwt({"user": user.username, "email": user.email})}
