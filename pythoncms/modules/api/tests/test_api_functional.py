import pytest
from init import db
from modules.contenttype.models import ContentType, ContentItem
import os

# We use fixtures from conftest.py: test_client, db, db_session

def test_get_types_empty(test_client):
    response = test_client.get("/api/v1/types")
    assert response.status_code == 200
    # Might not be empty if other tests or initialization added types
    # but in a clean testing.db it should be [] if we didn't add any in db fixture
    assert isinstance(response.json, list)

def test_get_content_not_found(test_client):
    response = test_client.get("/api/v1/nonexistent")
    assert response.status_code == 404
    assert "error" in response.json

def test_api_auth(test_client, monkeypatch):
    # Set API_TOKEN for testing auth
    monkeypatch.setenv("API_TOKEN", "test-token")
    
    # Unauthorized request (get_content checks auth)
    response = test_client.get("/api/v1/blog")
    assert response.status_code == 401
    
    # Authorized request
    headers = {"Authorization": "Bearer test-token"}
    response = test_client.get("/api/v1/blog", headers=headers)
    assert response.status_code == 404 # Content type not found, but not 401

def test_get_content_with_data(test_client):
    # Create content type and items
    ct = ContentType(name="blog", schema=[{"name": "title", "type": "text"}])
    db.session.add(ct)
    db.session.commit()
    
    item1 = ContentItem(content_type_id=ct.id, data={"title": "First"})
    item2 = ContentItem(content_type_id=ct.id, data={"title": "Second"})
    db.session.add_all([item1, item2])
    db.session.commit()
    
    response = test_client.get("/api/v1/blog")
    assert response.status_code == 200
    assert response.json["meta"]["total"] == 2
    assert len(response.json["data"]) == 2
    # Default order is desc by created_at, item2 was added last
    assert response.json["data"][0]["content"]["title"] == "Second"

def test_api_pagination(test_client):
    ct = ContentType(name="posts", schema=[{"name": "title", "type": "text"}])
    db.session.add(ct)
    db.session.commit()
    
    for i in range(5):
        db.session.add(ContentItem(content_type_id=ct.id, data={"title": str(i)}))
    db.session.commit()
    
    response = test_client.get("/api/v1/posts?limit=2&offset=0")
    assert response.status_code == 200
    assert response.json["meta"]["limit"] == 2
    assert len(response.json["data"]) == 2
    
    response = test_client.get("/api/v1/posts?limit=2&offset=4")
    assert len(response.json["data"]) == 1

def test_api_sorting(test_client):
    ct = ContentType(name="news", schema=[{"name": "title", "type": "text"}])
    db.session.add(ct)
    db.session.commit()
    
    item1 = ContentItem(content_type_id=ct.id, data={"title": "A"})
    item2 = ContentItem(content_type_id=ct.id, data={"title": "B"})
    db.session.add_all([item1, item2])
    db.session.commit()
    
    response = test_client.get("/api/v1/news?sort_by=id&order=asc")
    assert response.json["data"][0]["content"]["title"] == "A"
    
    response = test_client.get("/api/v1/news?sort_by=id&order=desc")
    assert response.json["data"][0]["content"]["title"] == "B"
