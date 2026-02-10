"""Test fixtures: in-memory SQLite database and FastAPI test client."""

# Patch SQLite to handle PostgreSQL-specific types BEFORE any app imports,
# because app.main creates tables at import time.
from sqlalchemy import JSON
from sqlalchemy.dialects.sqlite.base import SQLiteTypeCompiler

SQLiteTypeCompiler.visit_ARRAY = lambda self, type_, **kw: "JSON"
SQLiteTypeCompiler.visit_DOUBLE_PRECISION = lambda self, type_, **kw: "REAL"


import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient

from app.database import Base, get_db
from app.main import app
from app.models.property import Property, PropertyType, ListingStatus

# Replace PostgreSQL ARRAY with JSON on the photos column so SQLite can
# serialize/deserialize Python lists transparently.
Property.__table__.c.photos.type = JSON()

engine = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSession()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(autouse=True)
def setup_database():
    """Create all tables before each test, drop after."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def client():
    return TestClient(app)


@pytest.fixture()
def sample_property():
    """Insert a single property and return its id."""
    db = TestingSession()
    prop = Property(
        title="Test House",
        description="A nice test house",
        price=500000,
        address="123 Test St",
        city="Austin",
        state="TX",
        zip_code="78701",
        bedrooms=3,
        bathrooms=2.0,
        square_footage=1800,
        property_type=PropertyType.HOUSE,
        listing_status=ListingStatus.ACTIVE,
        photos=["https://example.com/photo.jpg"],
        latitude=30.2672,
        longitude=-97.7431,
    )
    db.add(prop)
    db.commit()
    db.refresh(prop)
    prop_id = prop.id
    db.close()
    return prop_id


@pytest.fixture()
def multiple_properties():
    """Insert several properties for filter tests."""
    db = TestingSession()
    props = [
        Property(
            title="Cheap Condo",
            description="Small condo downtown",
            price=200000,
            address="1 Main St",
            city="Denver",
            state="CO",
            zip_code="80202",
            bedrooms=1,
            bathrooms=1.0,
            square_footage=600,
            property_type=PropertyType.CONDO,
            listing_status=ListingStatus.ACTIVE,
            photos=[],
        ),
        Property(
            title="Mid-Range House",
            description="Family home in the suburbs",
            price=500000,
            address="50 Oak Ave",
            city="Austin",
            state="TX",
            zip_code="78701",
            bedrooms=3,
            bathrooms=2.5,
            square_footage=2000,
            property_type=PropertyType.HOUSE,
            listing_status=ListingStatus.ACTIVE,
            photos=[],
        ),
        Property(
            title="Luxury Penthouse",
            description="Penthouse with skyline views",
            price=2000000,
            address="100 Park Ave",
            city="Austin",
            state="TX",
            zip_code="78702",
            bedrooms=4,
            bathrooms=3.5,
            square_footage=3500,
            property_type=PropertyType.CONDO,
            listing_status=ListingStatus.SOLD,
            photos=[],
        ),
    ]
    db.add_all(props)
    db.commit()
    ids = [p.id for p in props]
    db.close()
    return ids
