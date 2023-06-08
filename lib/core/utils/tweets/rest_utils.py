import pydantic
from app.models.tweets import TweetLike
from app.models.users import User


def get_pydantic_from_mongo(
    pydantic_schema: pydantic.BaseModel, mongo_query_result, custom_mappings=None
) -> pydantic.BaseModel:
    mongo_query_dict = mongo_query_result.to_mongo()
    pydantic_dict = {}
    custom_mappings = custom_mappings if not None else {}
    for pydantic_key in pydantic_schema.__fields__.keys():
        if pydantic_key in custom_mappings.keys():
            pydantic_dict[pydantic_key] = custom_mappings[pydantic_key]
            continue
        if pydantic_key == "id":
            pydantic_dict["id"] = str(mongo_query_dict["_id"])
            continue
        pydantic_dict[pydantic_key] = mongo_query_dict[pydantic_key]
    pydantic_obj = pydantic_schema(**pydantic_dict)
    return pydantic_obj


def tweet_liked_by_user(tweet_id, username):
    try:
        user = User.objects.get(username=username)
        TweetLike.objects.get(tweet_id=tweet_id, user_id=user.id)
        return True
    except TweetLike.DoesNotExist:
        return False
