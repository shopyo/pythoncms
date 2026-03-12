import pytest
from init import db
from modules.contact.models import ContactMessage
from flask import url_for

def test_contact_index(test_client):
    response = test_client.get("/contact/")
    assert response.status_code == 200
    assert b"Contact" in response.data

def test_contact_submit_fail_no_auth(test_client):
    # validate_message requires login_required in view.py
    response = test_client.post("/contact/validate_message", data={
        "name": "Test",
        "email": "test@test.com",
        "message": "Hello"
    }, follow_redirects=True)
    # Redirects to login
    assert b"Login" in response.data

def test_contact_dashboard_no_auth(test_client):
    response = test_client.get("/contact/dashboard", follow_redirects=True)
    assert b"Login" in response.data

def test_contact_submit_and_dashboard(test_client, login_admin_user):
    # Now logged in as admin (from conftest.py login_admin_user fixture)
    response = test_client.post("/contact/validate_message", data={
        "name": "Test User",
        "email": "testuser@test.com",
        "message": "This is a test message"
    }, follow_redirects=True)
    
    # Check if message is in DB
    msg = ContactMessage.query.filter_by(email="testuser@test.com").first()
    assert msg is not None
    assert msg.name == "Test User"
    
    # Check dashboard
    response = test_client.get("/contact/dashboard")
    assert response.status_code == 200
    assert b"Test User" in response.data
    assert b"This is a test message" in response.data
