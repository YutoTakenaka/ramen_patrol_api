from fastapi import APIRouter, Depends, HTTPException
from typing import List
import schemas
from database import get_db
from sqlalchemy.orm import Session
from functions import post, auth

router = APIRouter(tags=["posts"])


# 投稿一覧取得
@router.get("/get_posts_all", response_model=List[schemas.Post])
def get_posts_all(db: Session = Depends(get_db)):
    return post.get_posts_all(db)


# 投稿取得
@router.get("/get_post/{post_id}", response_model=schemas.Post)
def get_post(
    post_id: int,
    db: Session = Depends(get_db),
):
    return post.get_post(post_id, db)


# 新規投稿
@router.post("/create_post", response_model=schemas.Post)
def create_post(
    request: schemas.CreatePost,
    db: Session = Depends(get_db),
):
    return post.create_post(request, db)


# 投稿編集
@router.post("/edit_post/{post_id}", response_model=schemas.Post)
def edit_post(
    request: schemas.UpdatePost,
    post_id: int,
    db: Session = Depends(get_db),
):
    return post.edit_post(request, post_id, db)


# 投稿削除
@router.post("/delete_post/{post_id}")
def delete_post(
    post_id,
    db: Session = Depends(get_db),
):
    return post.delete_post(post_id, db)
