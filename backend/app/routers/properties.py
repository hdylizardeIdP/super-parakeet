from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.property import Property, PropertyType
from app.schemas.property import PropertyOut

router = APIRouter(prefix="/api/properties", tags=["properties"])


@router.get("", response_model=list[PropertyOut])
def list_properties(
    min_price: Optional[int] = Query(None),
    max_price: Optional[int] = Query(None),
    city: Optional[str] = Query(None),
    state: Optional[str] = Query(None),
    bedrooms: Optional[int] = Query(None),
    property_type: Optional[str] = Query(None),
    search: Optional[str] = Query(None, max_length=200),
    db: Session = Depends(get_db),
):
    query = db.query(Property)

    if min_price is not None:
        query = query.filter(Property.price >= min_price)
    if max_price is not None:
        query = query.filter(Property.price <= max_price)
    if city:
        query = query.filter(Property.city.ilike(f"%{city}%"))
    if state:
        query = query.filter(Property.state.ilike(f"%{state}%"))
    if bedrooms is not None:
        query = query.filter(Property.bedrooms >= bedrooms)
    if property_type:
        query = query.filter(Property.property_type == property_type)
    if search:
        pattern = f"%{search}%"
        query = query.filter(
            Property.title.ilike(pattern)
            | Property.description.ilike(pattern)
            | Property.address.ilike(pattern)
            | Property.city.ilike(pattern)
        )

    return query.order_by(Property.id).all()


@router.get("/{property_id}", response_model=PropertyOut)
def get_property(property_id: int, db: Session = Depends(get_db)):
    return db.query(Property).filter(Property.id == property_id).first()
