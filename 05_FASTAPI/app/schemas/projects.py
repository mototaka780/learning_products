from pydantic import BaseModel
from datetime import date, datetime
from uuid import UUID
from pydantic import BaseModel, ConfigDict


# 共通フィールド
class ProjectBase(BaseModel):
    project_name: str
    project_type: str  # AI / ITインフラ / Web開発 / コンサル / BPO / その他
    budget: int | None = None
    description: str | None = None
    start_date: date | None = None
    end_date: date | None = None
    status: str | None = "ongoing"
    company_id: UUID


# 作成用
class ProjectCreate(ProjectBase):
    pass


# レスポンス用
class Project(ProjectBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
