from typing import Any, List, Union
from pydantic import BaseModel
from datetime import datetime


class Post(BaseModel):
    post_id: int
    image: str
    caption: str
    location: str
    created_at: datetime = None
    updated_at: datetime = None
    user_id: int

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


class User(BaseModel):
    user_id: int
    username: str
    mail: str
    created_at: datetime = None
    updated_at: datetime = None
    comments: List[Comment] = []
    posts: List[Post] = []

    class Config:
        orm_mode = True

