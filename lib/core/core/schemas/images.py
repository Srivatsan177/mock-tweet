from pydantic import BaseModel


class ImageInformationSchema(BaseModel):
    image_name: str
