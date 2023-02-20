from fastapi import HTTPException
from sqlalchemy.orm import Session
import models, schemas
from typing import List


# コメント取得
def get_comment(post_id: int, db: Session):
    query = (
        db.query(models.Comment, models.User)
        .join(models.User, models.Comment.user_id == models.User.user_id, isouter=True)
        .filter(models.Comment.post_id == post_id)
    )
    results = db.execute(query).all()
    if not results:
        raise HTTPException(status_code=404, detail="comment not found.")
    return [
        schemas.ResponseComment(comment=result[0], user=result[1]) for result in results
    ]


# コメント作成
def create_comment(request: schemas.CreateComment, db: Session):
    comment_dict = request.dict()
    comment = models.Comment(**comment_dict)
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment


# コメント削除
def delete_comment(comment_id: int, db=Session):
    comment = (
        db.query(models.Comment)
        .filter(models.Comment.comment_id == comment_id)
        .one_or_none()
    )
    if not comment:
        raise HTTPException(status_code=404, detail="comment not found.")

    # @todo ログインユーザーのuser_idと投稿したユーザーのuser_idが一致しているかチェック
    # if post.user_id != user_id:
    #     raise HTTPException(status_code = 403, detail = "This user does not have permission.")
    db.delete(comment)
    db.commit()
    return
