import pydantic


def get_pydantic_from_mongo(
    pydantic_schema: pydantic.BaseModel, mongo_query_result, mapping=None
) -> pydantic.BaseModel:
    if not mapping:
        mongo_query_dict = mongo_query_result.to_mongo()
        pydantic_dict = {}
        for pydantic_key in pydantic_schema.__fields__.keys():
            if pydantic_key == "id":
                pydantic_dict["id"] = str(mongo_query_dict["_id"])
                continue
            pydantic_dict[pydantic_key] = mongo_query_dict[pydantic_key]
        pydantic_obj = pydantic_schema(**pydantic_dict)
    else:
        pass
    return pydantic_obj
