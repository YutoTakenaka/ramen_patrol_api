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


class CreateComment(BaseModel):
    comment: str
    post_id: int
    user_id: int


class Comment(CreateComment):
    comment_id: int
    created_at: datetime = None
    updated_at: datetime = None

    class Config:
        orm_mode = True


class CreateUser(BaseModel):
    username: str
    password: str


class User(BaseModel):
    user_id: int
    username: str
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


class ResponseComment(BaseModel):
    comment: Comment
    user: User


class ResponsePost(BaseModel):
    post: Post
    user: User
