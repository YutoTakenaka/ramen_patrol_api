from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from database import Base
from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import relationship

JST = timezone(timedelta(hours=+9), "JST")


class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String, index=True)
    created_at = Column(DateTime, default=datetime.now(JST), nullable=True)
    updated_at = Column(DateTime, default=datetime.now(JST), nullable=True)
    user_posts = relationship("Post", back_populates="post_user")
    user_comments = relationship("Comment", back_populates="comment_user")

    def __init__(self, username):
        self.username = username


class Post(Base):
    __tablename__ = "posts"
    post_id = Column(Integer, primary_key=True, index=True)
    # @todo imageの型をファイル型に修正
    image = Column(String, index=True)
    # image = Column(UploadFile, index=True)
    caption = Column(String, index=True)
    location = Column(String, index=True)
    created_at = Column(DateTime, default=datetime.now(JST), nullable=True)
    updated_at = Column(DateTime, default=datetime.now(JST), nullable=True)
    user_id = Column(
        Integer,
        ForeignKey("users.user_id", ondelete="SET NULL"),
        nullable=False,
        index=True,
    )
    post_user = relationship("User", back_populates="user_posts")
    post_comments = relationship("Comment", back_populates="comment_post")


class Comment(Base):
    __tablename__ = "comments"
    comment_id = Column(Integer, primary_key=True, index=True)
    comment = Column(String, index=True)
    created_at = Column(DateTime, default=datetime.now(JST), nullable=True)
    updated_at = Column(DateTime, default=datetime.now(JST), nullable=True)
    user_id = Column(
        Integer,
        ForeignKey("users.user_id", ondelete="SET NULL"),
        nullable=False,
        index=True,
    )
    post_id = Column(
        Integer,
        ForeignKey("posts.post_id", ondelete="SET NULL"),
        nullable=False,
        index=True,
    )
    comment_user = relationship("User", back_populates="user_comments")
    comment_post = relationship("Post", back_populates="post_comments")
