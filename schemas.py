from typing import List
from pydantic import BaseModel
from datetime import datetime
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm


class CreatePost(BaseModel):
    # @todo imageの型をファイルに合った型に修正
    image: str
    caption: str
    location: str
    user_id: int


class UpdatePost(CreatePost):
    post_id: int


class Post(CreatePost):
    post_id: int
    created_at: datetime = None
    updated_at: datetime = None

    class Config:
        orm_mode = True


class Comment(BaseModel):
    comment_id: int
    comment: str
    user_id: int
    post_id: int
    updated_at: datetime = None

    class Config:
        orm_mode = True


class CreateUser(BaseModel):
    username: str
    password: str


class User(BaseModel):
    user_id: int
    username: str
    # mail: str
    created_at: datetime = None
    updated_at: datetime = None
    comments: List[Comment] = []
    posts: List[Post] = []

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str
    user_id: int
    username: str


class TokenData(BaseModel):
    username: str


class UserInDB(User):
    hashed_password: str
