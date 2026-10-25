from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from database import Base

class Project(Base):
    __tablename__ = "projects"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # FK → companies.id（UUID）
    company_id = Column(UUID(as_uuid=True), ForeignKey("companies.id"), nullable=False)

    project_name = Column(String, nullable=False)
    project_type = Column(String, nullable=False)  # AI / ITインフラ / Web開発 / コンサル / BPO / その他
    budget = Column(Integer, nullable=True)
    description = Column(String, nullable=True)

    start_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)

    status = Column(String, default="ongoing")

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

    # リレーション（案件 → 企業）
    company = relationship("Company", back_populates="projects")

