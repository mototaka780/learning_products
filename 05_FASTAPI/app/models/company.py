from sqlalchemy import Column, String, Integer, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID
import uuid

from database import Base

class Company(Base):
    __tablename__ = "companies"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    company_name = Column(String(100), nullable=False)
    industry = Column(String(50))
    city = Column(String(50))
    country = Column(String(50))
    employee_count = Column(Integer)
    website = Column(String(255))
    notes = Column(String(500))

    # ★ 追加：作成したユーザーの ID
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)

    # ★ 追加：作成日時
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # ★ 追加：更新日時
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
