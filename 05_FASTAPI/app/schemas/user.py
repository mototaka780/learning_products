from pydantic import BaseModel, Field
from uuid import UUID


class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6)
    role: str = "user"  # ★ 追加

class UserResponse(BaseModel):
    id: UUID
    username: str
    role: str

    model_config = {
        "from_attributes": True
    }

