import pytest

def test_www_index(test_client):
    response = test_client.get("/")
    assert response.status_code == 200
    # Editorial theme default title check
    assert b"Editorial" in response.data or b"Hyperspace" in response.data
