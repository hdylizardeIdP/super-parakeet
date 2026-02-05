from typing import Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field


class ContactCreate(BaseModel):
    property_id: int
    name: str = Field(..., min_length=1, max_length=200)
    email: EmailStr
    phone: Optional[str] = Field(None, max_length=30)
    message: str = Field(..., min_length=1, max_length=5000)


class ContactOut(BaseModel):
    id: int
    property_id: int
    name: str
    email: str
    phone: Optional[str] = None
    message: str
    created_at: datetime

    class Config:
        from_attributes = True
