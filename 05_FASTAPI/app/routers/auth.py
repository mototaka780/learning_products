from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from crud.user import create_user, get_user_by_username
from utils.security import verify_password
from database import get_db
from schemas.user import UserCreate, UserResponse
from schemas.auth import LoginRequest, TokenResponse
from utils.jwt import create_access_token
from utils.jwt import get_current_user as jwt_current_user


router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

auth_scheme = HTTPBearer()


# =========================================================
# 認証済みユーザー取得
# =========================================================
def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(auth_scheme)
):
    user = jwt_current_user(credentials.credentials)

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )

    return user


# =========================================================
# ユーザー登録
# =========================================================
@router.post(
    "/register",
    response_model=UserResponse
)
def register(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    existing = get_user_by_username(
        db,
        user.username
    )

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Username already exists"
        )

    new_user = create_user(
        db,
        user
    )

    return new_user


# =========================================================
# ログイン
# =========================================================
@router.post(
    "/login",
    response_model=TokenResponse
)
def login(
    request: LoginRequest,
    db: Session = Depends(get_db)
):
    user = get_user_by_username(
        db,
        request.username
    )

    if not user or not verify_password(
        request.password,
        user.hashed_password
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    token = create_access_token({
        "sub": str(user.id),
        "role": user.role,
    })

    return TokenResponse(
        access_token=token,
        token_type="bearer"
    )


# =========================================================
# 自分のユーザー情報
# =========================================================
@router.get("/me")
def read_me(
    user=Depends(get_current_user)
):
    return {
        "username": user.username,
        "role": user.role
    }