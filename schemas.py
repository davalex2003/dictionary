from pydantic import BaseModel


class User(BaseModel):
    login: str
    hash_password: str


class UserLogin(BaseModel):
    login: str
