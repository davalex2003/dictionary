from pydantic import BaseModel


class User(BaseModel):
    login: str
    hash_password: str


class UserID(BaseModel):
    id: int


class Dictionary(BaseModel):
    id: int
    name: str


class DictionaryDTO(BaseModel):
    name: str
    user_id: int
    glosses: dict
