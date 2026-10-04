import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from uuid import UUID

from database import Base, get_db
from main import app
from routers.auth import get_current_user
from models.company import Company
from models.user import User


TEST_DATABASE_URL = (
    "postgresql://postgres:moto0204Z%40@localhost:5432/india_market_test_db"
)

engine = create_engine(
    TEST_DATABASE_URL,
    pool_pre_ping=True,
    echo=False
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base.metadata.create_all(bind=engine)


class FakeUser:
    id = UUID("00000000-0000-0000-0000-000000000000")
    username = "test_user"
    role = "admin"


@pytest.fixture
def db():
    session = TestingSessionLocal()

    try:
        # 既存データ削除
        # Company.user_id → User.id の外部キーがあるため、
        # Userより先にCompanyを削除する
        session.execute(Company.__table__.delete())
        session.execute(User.__table__.delete())

        # pytest用のテストユーザーをPostgreSQLに登録
        test_user = User(
            id=UUID("00000000-0000-0000-0000-000000000000"),
            username="test_user",
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

    with TestClient(app) as client:
        yield client

    app.dependency_overrides.clear()