# database.py
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# 1. 環境変数から読み込む
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    # ローカル開発用のデフォルト
    DATABASE_URL = "postgresql://postgres:moto0204Z%40@localhost:5432/india_market_db"

# 2. エンジン作成
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    echo=False
)

# 3. セッション
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# 4. Base
Base = declarative_base()

# 5. FastAPI 用の依存関係
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
