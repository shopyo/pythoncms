import pytest
from init import db
from modules.contenttype.models import ContentType, ContentItem
from flask import url_for

def test_contenttype_dashboard_no_auth(test_client):
    response = test_client.get("/contenttype/dashboard", follow_redirects=True)
    assert b"Login" in response.data

def test_contenttype_flow(test_client, login_admin_user):
    # 1. Create a Content Type
    import uuid
    type_name = f"blog_{uuid.uuid4().hex[:8]}"
    response = test_client.post("/contenttype/create", data={
        "name": type_name,
        "description": "Blog posts",
        "field_name[]": ["title", "content"],
        "field_type[]": ["text", "richtext"]
    }, follow_redirects=True)
    
    assert response.status_code == 200
    
    ct = ContentType.query.filter_by(name=type_name).first()
    assert ct is not None
    assert ct is not None
    assert len(ct.schema) == 2
    
    # 2. Add an item
    response = test_client.post(f"/contenttype/type/{ct.id}/item/add", data={
        "title": "Hello World",
        "content": "<p>This is a test</p>"
    }, follow_redirects=True)
    
    assert b"Item added" in response.data
    
    item = ContentItem.query.filter_by(content_type_id=ct.id).first()
    assert item is not None
    assert item.data["title"] == "Hello World"
    
    # 3. Edit the item
    response = test_client.post(f"/contenttype/item/{item.id}/edit", data={
        "title": "Hello Edited",
        "content": "<p>Edited content</p>"
    }, follow_redirects=True)
    
    assert b"Item updated" in response.data
    db.session.refresh(item)
    assert item.data["title"] == "Hello Edited"
    
    # 4. Delete item
    response = test_client.get(f"/contenttype/item/{item.id}/delete", follow_redirects=True)
    assert b"Item deleted" in response.data
    assert ContentItem.query.get(item.id) is None
    
    # 5. Delete type
    response = test_client.get(f"/contenttype/type/{ct.id}/delete", follow_redirects=True)
    assert b"Content Type deleted" in response.data
    assert ContentType.query.get(ct.id) is None

def test_create_type_invalid(test_client, login_admin_user):
    # Missing name
    response = test_client.post("/contenttype/create", data={
        "field_name[]": ["title"],
        "field_type[]": ["text"]
    }, follow_redirects=True)
    assert b"Name and at least one field are required" in response.data
