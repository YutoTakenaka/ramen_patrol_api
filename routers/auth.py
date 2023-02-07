from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends, HTTPException, status
from database import get_db
from sqlalchemy.orm import Session
from functions import auth
import schemas, models
from datetime import timedelta


ACCESS_TOKEN_EXPIRE_MINUTES = 120
router = APIRouter(tags=["token"])


# サインアップ
@router.post("/signup", response_model=schemas.Token)
async def signup(request: schemas.CreateUser, db: Session = Depends(get_db)):
    user = auth.create_user(db, request)
    # トークンの有効期限を指定
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": user.user_id,
        "username": user.username,
    }


# ログイン認証
@router.post("/token", response_model=schemas.Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    user = (
        db.query(models.User)
        .filter(models.User.username == form_data.username)
        .one_or_none()
    )
    # ユーザーが存在するかチェック
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # パスワードが一致するかチェック
    password = form_data.password
    if not password == user.password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    # トークンの有効期限を指定
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": user.user_id,
        "username": user.username,
    }


@router.get("/users/me/", response_model=schemas.User)
async def read_users_me(
    current_user: schemas.User = Depends(auth.get_current_active_user),
):
    return current_user


# @router.get("/users/me/items/")
# async def read_own_items(
#     current_user: schemas.User = Depends(auth.get_current_active_user),
# ):
#     return [{"item_id": "Foo", "owner": current_user.username}]
