import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)

def test_signup_for_activity():
    # Use a valid activity name from the app
    activities = client.get("/activities").json()
    activity_name = next(iter(activities))
    email = "testuser@mergington.edu"
    response = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert response.status_code == 200
    assert "message" in response.json()

    # Try to sign up again (should fail if duplicate check is implemented)
    response2 = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert response2.status_code != 200 or "detail" in response2.json()

def test_unregister_for_activity():
    activities = client.get("/activities").json()
    activity_name = next(iter(activities))
    email = "testuser@mergington.edu"
    # Register first
    client.post(f"/activities/{activity_name}/signup?email={email}")
    # Unregister
    response = client.post(f"/activities/{activity_name}/unregister?email={email}")
    assert response.status_code == 200 or response.status_code == 204
