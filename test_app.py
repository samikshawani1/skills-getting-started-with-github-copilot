from fastapi.testclient import TestClient

from src.app import app, activities

client = TestClient(app)


def test_delete_participant_removes_email():
    original_participants = activities["Chess Club"]["participants"][:]

    try:
        response = client.delete(
            "/activities/Chess Club/participants?email=daniel@mergington.edu"
        )

        assert response.status_code == 200
        assert response.json()["message"] == "Removed daniel@mergington.edu from Chess Club"
        assert "daniel@mergington.edu" not in activities["Chess Club"]["participants"]
    finally:
        activities["Chess Club"]["participants"] = original_participants


def test_delete_participant_missing_returns_404():
    response = client.delete(
        "/activities/Chess Club/participants?email=missing@mergington.edu"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found"
