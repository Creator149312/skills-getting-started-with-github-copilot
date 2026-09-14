from fastapi.testclient import TestClient

from src.app import app, activities

client = TestClient(app)


def test_unregister_participant_from_activity():
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"

    activities[activity_name]["participants"].append(email)

    response = client.delete(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )

    assert response.status_code == 200
    assert email not in activities[activity_name]["participants"]
    assert response.json()["message"] == f"Removed {email} from {activity_name}"


def test_unregister_missing_participant_returns_error():
    activity_name = "Chess Club"
    email = "missingstudent@mergington.edu"

    response = client.delete(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )

    assert response.status_code == 400
    assert "not signed up" in response.json()["detail"].lower()
