from typing import Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr


class ContactCreate(BaseModel):
    property_id: int
    name: str
    email: str
    phone: Optional[str] = None
    message: str


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
