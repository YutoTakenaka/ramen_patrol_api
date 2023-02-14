from fastapi import HTTPException
from sqlalchemy.orm import Session
import models, schemas
from datetime import datetime


# コメント取得
def get_comment(post_id: int, db: Session):
    return db.query(models.Comment).filter(models.Comment.post_id == post_id).all()


# コメント作成
def create_comment(request: schemas.CreateComment, db: Session):
    comment_dict = request.dict()
    comment = models.Comment(**comment_dict)
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment
