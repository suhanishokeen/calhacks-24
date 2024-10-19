from pydantic import BaseModel
from bson import ObjectId

# User schema
class User(BaseModel):
    username: str
    email: str
    password: str