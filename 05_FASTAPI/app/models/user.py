from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
import uuid

from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String(50), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)

    # ★ 追加：ロール（admin / user）
    role = Column(String(20), nullable=False, default="user")
