from fastapi import APIRouter, Depends, Header
from typing import List
import schemas
from ..database import get_db
from sqlalchemy.orm import Session
from functions import post

# dbを生成している
# models.Base.metadata.create_all(bind=engine)

router = APIRouter()

# 投稿一覧取得
@router.get("/get_posts", response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db)):
    return post.get_posts(db)