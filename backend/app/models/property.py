from sqlalchemy import Column, Integer, String, Float, Text, Enum as SAEnum, ARRAY
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION
import enum

from app.database import Base


class PropertyType(str, enum.Enum):
    HOUSE = "House"
    CONDO = "Condo"
    TOWNHOUSE = "Townhouse"
    APARTMENT = "Apartment"
    LAND = "Land"
    COMMERCIAL = "Commercial"


class ListingStatus(str, enum.Enum):
    ACTIVE = "Active"
    PENDING = "Pending"
    SOLD = "Sold"


class Property(Base):
    __tablename__ = "properties"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    price = Column(Integer, nullable=False)
    address = Column(String(500), nullable=False)
    city = Column(String(100), nullable=False)
    state = Column(String(50), nullable=False)
    zip_code = Column(String(10), nullable=False)
    bedrooms = Column(Integer, nullable=False)
    bathrooms = Column(Float, nullable=False)
    square_footage = Column(Integer, nullable=False)
    property_type = Column(SAEnum(PropertyType), nullable=False)
    listing_status = Column(SAEnum(ListingStatus), nullable=False, default=ListingStatus.ACTIVE)
    photos = Column(ARRAY(String), default=[])
    latitude = Column(DOUBLE_PRECISION, nullable=True)
    longitude = Column(DOUBLE_PRECISION, nullable=True)
