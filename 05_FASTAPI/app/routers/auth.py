from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import SessionLocal
from crud.user import create_user, get_user_by_username
from schemas.user import UserCreate, UserResponse
from schemas.auth import LoginRequest, TokenResponse
from utils.security import verify_password
from utils.jwt import create_access_token, get_current_user   # ★ 追加
from fastapi.security import OAuth2PasswordBearer
from fastapi.security import HTTPBearer

#oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
auth_scheme = HTTPBearer()

router = APIRouter(prefix="/auth", tags=["Auth"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/register", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing = get_user_by_username(db, user.username)
    if existing:
        raise HTTPException(status_code=400, detail="Username already exists")

    new_user = create_user(db, user)
    return new_user


@router.post("/login", response_model=TokenResponse)
def login(request: LoginRequest, db: Session = Depends(get_db)):
    user = get_user_by_username(db, request.username)

    if not user:
        raise HTTPException(status_code=400, detail="Invalid username or password")

    if not verify_password(request.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid username or password")

    token = create_access_token({
    "sub": str(user.id),   # ★ UUID を入れる
    "role": user.role,
    })

    return TokenResponse(access_token=token, token_type="bearer")

@router.get("/me")
def read_me(token: str = Depends(auth_scheme)):
    user = get_current_user(token.credentials)
    return {"username": user.username, "role": user.role}


