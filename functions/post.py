from fastapi import HTTPException
from sqlalchemy.orm import Session
import models, schemas

# 投稿一覧取得
def get_posts(db: Session):
    return db.query(models.Post).order_by(models.Post.created_at.desc()).all()
