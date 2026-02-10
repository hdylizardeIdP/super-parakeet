"""Tests for the contact inquiry API endpoint."""


def test_create_inquiry(client, sample_property):
    resp = client.post("/api/contact", json={
        "property_id": sample_property,
        "name": "Jane Doe",
        "email": "jane@example.com",
        "phone": "555-1234",
        "message": "I'd like to schedule a viewing.",
    })
    assert resp.status_code == 201
    data = resp.json()
    assert data["name"] == "Jane Doe"
    assert data["email"] == "jane@example.com"
    assert data["property_id"] == sample_property
    assert "id" in data
    assert "created_at" in data


def test_create_inquiry_without_phone(client, sample_property):
    resp = client.post("/api/contact", json={
        "property_id": sample_property,
        "name": "John Doe",
        "email": "john@example.com",
        "message": "Is this still available?",
    })
    assert resp.status_code == 201
    assert resp.json()["phone"] is None


def test_create_inquiry_invalid_property(client):
    resp = client.post("/api/contact", json={
        "property_id": 9999,
        "name": "Jane Doe",
        "email": "jane@example.com",
        "message": "Hello",
    })
    assert resp.status_code == 404
    assert resp.json()["detail"] == "Property not found"


def test_create_inquiry_invalid_email(client, sample_property):
    resp = client.post("/api/contact", json={
        "property_id": sample_property,
        "name": "Jane Doe",
        "email": "not-an-email",
        "message": "Hello",
    })
    assert resp.status_code == 422


def test_create_inquiry_missing_name(client, sample_property):
    resp = client.post("/api/contact", json={
        "property_id": sample_property,
        "email": "jane@example.com",
        "message": "Hello",
    })
    assert resp.status_code == 422


def test_create_inquiry_empty_message(client, sample_property):
    resp = client.post("/api/contact", json={
        "property_id": sample_property,
        "name": "Jane Doe",
        "email": "jane@example.com",
        "message": "",
    })
    assert resp.status_code == 422
