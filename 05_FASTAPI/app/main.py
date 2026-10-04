from fastapi import FastAPI
from database import Base, engine
from routers.company import router as company_router
from routers.auth import router as auth_router   # ★ 追加
import os


# テーブル作成（学習用）
if os.getenv("ENV") != "test":
    Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="India Market Research API",
    version="1.0.0"
)

# ★ 認証ルーターを追加
app.include_router(auth_router)

# 会社ルーター
app.include_router(company_router)

@app.get("/")
def root():
    return {"message": "India Market Research API"}
