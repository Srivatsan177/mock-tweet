from pydantic import BaseModel
from typing import *
from hashlib import sha256

class UserSignupSchema(BaseModel):
    email: str
    username: str
    name: str
    password: str
    
    @property
    def password_hash(self):
        return sha256(self.password.encode()).hexdigest()
    
    # @property
    # def mongo_document(self):
    #     return {
    #         "email": self.email,
    #         "username": self.username,
    #         "name": self.name,
    #         "password": self.password_hash,
    #     }

