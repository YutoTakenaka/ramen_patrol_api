from fastapi import HTTPException
from sqlalchemy.orm import Session
import models, schemas

# 投稿一覧取得
def get_posts_all(db: Session):
    return db.query(models.Post).order_by(models.Post.created_at.desc()).all()

# 新規投稿
def create_post(request: schemas.CreatePost, db: Session):
    post_dict = request.dict()
    post = models.Post(**post_dict)
    db.add(post)
    db.commit()
    return post

