from fastapi import APIRouter, Depends
from typing import List
import schemas
from database import get_db
from sqlalchemy.orm import Session
from functions import post

router = APIRouter(tags=["posts"])

# 投稿一覧取得
@router.get("/get_posts_all", response_model=List[schemas.Post])
def get_posts_all(db: Session = Depends(get_db)):
    return post.get_posts_all(db)

# 新規投稿
@router.post("/create_post", response_model = schemas.Post)
def create_post(request: schemas.CreatePost,db: Session = Depends(get_db)):
    return post.create_post(request, db)

# 投稿編集
@router.post("/edit_post", response_model = schemas.Post)
def edit_post(request: schemas.UpdatePost,db: Session = Depends(get_db)):
    return post.edit_post(request, db)