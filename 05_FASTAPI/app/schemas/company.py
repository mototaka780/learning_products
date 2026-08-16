from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field, HttpUrl
from enum import Enum

class IndustryEnum(str, Enum):
    it = "IT"
    finance = "Finance"
    manufacturing = "Manufacturing"
    retail = "Retail"
    healthcare = "Healthcare"

class CountryEnum(str, Enum):
    japan = "Japan"
    india = "India"
    usa = "USA"
    uk = "UK"
    germany = "Germany"
    france = "France"
    china = "China"
    south_korea = "South Korea"
    singapore = "Singapore"
    australia = "Australia"
    
class CompanyCreate(BaseModel):
    company_name: str = Field(..., min_length=1, max_length=100)
    industry: IndustryEnum
    city: str = Field(..., min_length=1, max_length=50)
    country: CountryEnum
    employee_count: int = Field(..., ge=0)
    website: HttpUrl | None = None
    notes: str | None = Field(None, max_length=500)


class CompanyUpdate(BaseModel):
    company_name: str | None = Field(None, min_length=1, max_length=100)
    industry: IndustryEnum | None = None
    city: str | None = Field(None, min_length=1, max_length=50)
    country: CountryEnum | None = None
    employee_count: int | None = Field(None, ge=0)
    website: HttpUrl | None = None
    notes: str | None = Field(None, max_length=500)



class CompanyResponse(BaseModel):
    id: UUID
    company_name: str
    industry: IndustryEnum | None
    city: str | None
    country: CountryEnum
    employee_count: int | None
    website: HttpUrl | None   # ★ 修正ポイント
    notes: str | None
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True
    }