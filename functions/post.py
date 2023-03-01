from fastapi import HTTPException
from sqlalchemy.orm import Session
import models, schemas
from datetime import datetime


# 投稿一覧取得
def get_posts_all(db: Session):
    query = db.query(models.Post, models.User).join(
        models.User, models.Post.user_id == models.User.user_id, isouter=True
    )
    results = db.execute(query).all()
    if not results:
        raise HTTPException(status_code=404, detail="post not found.")
    return [schemas.ResponsePost(post=result[0], user=result[1]) for result in results]


# 投稿取得
def get_post(post_id: int, db: Session):
    query = (
        db.query(models.Post, models.User)
        .join(models.User, models.Post.user_id == models.User.user_id, isouter=True)
        .filter(models.Post.post_id == post_id)
    )

    results = db.execute(query)
    if not results:
        raise HTTPException(status_code=404, detail="post not found.")
    return [schemas.ResponsePost(post=result[0], user=result[1]) for result in results]


# 新規投稿
def create_post(request: schemas.CreatePost, db: Session):
    post_dict = request.dict()
    post = models.Post(**post_dict)
    db.add(post)
    db.commit()
    db.refresh(post)
    return post


# 投稿編集
def edit_post(request: schemas.UpdatePost, post_id: int, db: Session):
    post = db.query(models.Post).filter(models.Post.post_id == post_id).one_or_none()
    if not post:
        raise HTTPException(status_code=404, detail="post_id not found.")

    if post.user_id != request.user_id:
        raise HTTPException(
            status_code=403, detail="This user does not have permission."
        )
    post.image = request.image
    if post.image == "":
        raise HTTPException(status_code=400, detail="Image is required.")
    post.caption = request.caption
    post.location = request.location
    post.updated_at = datetime.now(models.JST)

    db.commit()
    return post


# 投稿削除
def delete_post(post_id: int, db=Session):
    post = db.query(models.Post).filter(models.Post.post_id == post_id).one_or_none()
    if not post:
        raise HTTPException(status_code=404, detail="post not found.")
    # @todo ログインユーザーのuser_idと投稿したユーザーのuser_idが一致しているかチェック
    # if post.user_id != user_id:
    #     raise HTTPException(status_code = 403, detail = "This user does not have permission.")
    db.delete(post)
    db.commit()
    return
