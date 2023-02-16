from fastapi import APIRouter, Depends
from typing import List
import schemas
from database import get_db
from sqlalchemy.orm import Session
from functions import comment

router = APIRouter(tags=["comments"])


# コメント取得
@router.get("/get_comment/{post_id}", response_model=List[schemas.Comment])
def get_post(post_id, db: Session = Depends(get_db)):
    return comment.get_comment(post_id, db)


# コメント作成
@router.post("/create_comment", response_model=schemas.Comment)
def create_comment(request: schemas.CreateComment, db: Session = Depends(get_db)):
    return comment.create_comment(request, db)


# コメント削除
@router.post("/delete_comment/{comment_id}")
def delete_comment(comment_id, db: Session = Depends(get_db)):
    return comment.delete_comment(comment_id, db)
