from fastapi import HTTPException
from sqlalchemy.orm import Session
import models, schemas
from datetime import datetime

# 投稿一覧取得
def get_posts_all(db: Session):
    return db.query(models.Post).order_by(models.Post.created_at.desc()).all()


# 新規投稿
def create_post(request: schemas.CreatePost, db: Session):
    post_dict = request.dict()
    post = models.Post(**post_dict)
    db.add(post)
    db.commit()
    db.refresh(post)
    return post


# 投稿編集
def edit_post(request: schemas.UpdatePost, db: Session):
    post_id = request.post_id
    post = db.query(models.Post).filter(models.Post.post_id == post_id).first()
    if not post:
        raise HTTPException(status_code = 404, detail = "post_id not found.")
    
    if post.user_id != request.user_id:
        raise HTTPException(status_code = 403, detail = "This user does not have permission.")

    post.image = request.image
    if post.image == "":
        raise HTTPException(status_code = 400, detail = "Image is required.")
    post.caption = request.caption
    post.location = request.location
    post.updated_at = datetime.now(models.JST)

    db.commit()
    db.refresh(post)
    return post