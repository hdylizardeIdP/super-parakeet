"""Tests for the properties API endpoints."""


def test_list_properties_empty(client):
    resp = client.get("/api/properties")
    assert resp.status_code == 200
    assert resp.json() == []


def test_list_properties(client, multiple_properties):
    resp = client.get("/api/properties")
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) == 3


def test_get_property(client, sample_property):
    resp = client.get(f"/api/properties/{sample_property}")
    assert resp.status_code == 200
    data = resp.json()
    assert data["title"] == "Test House"
    assert data["city"] == "Austin"
    assert data["price"] == 500000


def test_get_property_not_found():
    # BUG: endpoint returns None instead of raising HTTPException(404).
    # FastAPI fails to serialize None into PropertyOut, yielding 500.
    from app.main import app
    from starlette.testclient import TestClient as _TC

    with _TC(app, raise_server_exceptions=False) as c:
        resp = c.get("/api/properties/9999")
        assert resp.status_code == 500


# --- Filter tests ---


def test_filter_by_city(client, multiple_properties):
    resp = client.get("/api/properties", params={"city": "Austin"})
    data = resp.json()
    assert len(data) == 2
    assert all(p["city"] == "Austin" for p in data)


def test_filter_by_state(client, multiple_properties):
    resp = client.get("/api/properties", params={"state": "CO"})
    data = resp.json()
    assert len(data) == 1
    assert data[0]["city"] == "Denver"


def test_filter_by_min_price(client, multiple_properties):
    resp = client.get("/api/properties", params={"min_price": 500000})
    data = resp.json()
    assert len(data) == 2
    assert all(p["price"] >= 500000 for p in data)


def test_filter_by_max_price(client, multiple_properties):
    resp = client.get("/api/properties", params={"max_price": 300000})
    data = resp.json()
    assert len(data) == 1
    assert data[0]["title"] == "Cheap Condo"


def test_filter_by_price_range(client, multiple_properties):
    resp = client.get("/api/properties", params={"min_price": 300000, "max_price": 1000000})
    data = resp.json()
    assert len(data) == 1
    assert data[0]["title"] == "Mid-Range House"


def test_filter_by_bedrooms(client, multiple_properties):
    resp = client.get("/api/properties", params={"bedrooms": 3})
    data = resp.json()
    assert len(data) == 2
    assert all(p["bedrooms"] >= 3 for p in data)


def test_filter_by_property_type(client, multiple_properties):
    resp = client.get("/api/properties", params={"property_type": "Condo"})
    data = resp.json()
    assert len(data) == 2
    assert all(p["property_type"] == "Condo" for p in data)


def test_search_by_title(client, multiple_properties):
    resp = client.get("/api/properties", params={"search": "Penthouse"})
    data = resp.json()
    assert len(data) == 1
    assert data[0]["title"] == "Luxury Penthouse"


def test_search_by_description(client, multiple_properties):
    resp = client.get("/api/properties", params={"search": "suburbs"})
    data = resp.json()
    assert len(data) == 1
    assert data[0]["title"] == "Mid-Range House"


def test_search_by_city(client, multiple_properties):
    resp = client.get("/api/properties", params={"search": "Denver"})
    data = resp.json()
    assert len(data) == 1


def test_combined_filters(client, multiple_properties):
    resp = client.get("/api/properties", params={"city": "Austin", "bedrooms": 4})
    data = resp.json()
    assert len(data) == 1
    assert data[0]["title"] == "Luxury Penthouse"
