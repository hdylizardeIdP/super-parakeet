from typing import Optional
from pydantic import BaseModel


class PropertyOut(BaseModel):
    id: int
    title: str
    description: str
    price: int
    address: str
    city: str
    state: str
    zip_code: str
    bedrooms: int
    bathrooms: float
    square_footage: int
    property_type: str
    listing_status: str
    photos: list[str]
    latitude: Optional[float] = None
    longitude: Optional[float] = None

    class Config:
        from_attributes = True


class PropertyFilter(BaseModel):
    min_price: Optional[int] = None
    max_price: Optional[int] = None
    city: Optional[str] = None
    state: Optional[str] = None
    bedrooms: Optional[int] = None
    property_type: Optional[str] = None
    search: Optional[str] = None
