
import os
from uuid import UUID

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# main.py のインポート時に開発DBの create_all() が
# 実行されないよう、先にテストモードを指定する
os.environ["ENV"] = "test"

from database import Base, get_db

# モデルを明示的に読み込み、テーブルをmetadataに登録する
from models.user import User
from models.company import Company
from models.projects import Project

from routers.auth import get_current_user
from main import app


# Docker Compose の環境変数から取得する
TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL")

if not TEST_DATABASE_URL:
    raise RuntimeError(
        "TEST_DATABASE_URL が未設定です。"
        "docker-compose.yml の api.environment を確認してください。"
    )

# 接続先DB名を事前チェック
database_name = TEST_DATABASE_URL.split("?", 1)[0].rsplit("/", 1)[-1]

if database_name != "india_market_test_db":
    raise RuntimeError(
        "テストを中止しました。"
        f"接続先DB名が想定外です: {database_name}"
    )

engine = create_engine(
    TEST_DATABASE_URL,
    pool_pre_ping=True,
    echo=False,
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

# 実際に接続したDB名も確認
with engine.connect() as connection:
    actual_database = connection.execute(
        text("SELECT current_database()")
    ).scalar_one()

if actual_database != "india_market_test_db":
    engine.dispose()
    raise RuntimeError(
        f"想定外のDBに接続しました: {actual_database}"
    )

# テストDBにテーブルを作成する
Base.metadata.create_all(bind=engine)


class FakeUser:
    id = UUID("00000000-0000-0000-0000-000000000000")
    username = "test_user"
    role = "admin"


@pytest.fixture
def db():
    session = TestingSessionLocal()

    try:
        # 外部キー制約に配慮し、子テーブルから削除する
        session.execute(Project.__table__.delete())
        session.execute(Company.__table__.delete())
        session.execute(User.__table__.delete())

        test_user = User(
            id=FakeUser.id,
            username=FakeUser.username,
            hashed_password="test_password",
            role="admin",
        )

        session.add(test_user)
        session.commit()

        yield session

    finally:
        session.close()


@pytest.fixture
def client(db):
    app.dependency_overrides[get_db] = lambda: db
    app.dependency_overrides[get_current_user] = lambda: FakeUser()

    try:
        with TestClient(app) as test_client:
            yield test_client
    finally:
        app.dependency_overrides.clear()
