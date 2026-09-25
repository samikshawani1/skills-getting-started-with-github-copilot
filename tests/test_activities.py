from fastapi.testclient import TestClient

from src.app import activities, app

client = TestClient(app)


def test_delete_participant_removes_email():
    # Arrange
    activity_name = "Chess Club"
    email_to_remove = "daniel@mergington.edu"
    original_participants = activities[activity_name]["participants"][:]

    try:
        # Act
        response = client.delete(
            f"/activities/{activity_name}/participants?email={email_to_remove}"
        )

        # Assert
        assert response.status_code == 200
        assert response.json()["message"] == (
            f"Removed {email_to_remove} from {activity_name}"
        )
        assert email_to_remove not in activities[activity_name]["participants"]
    finally:
        activities[activity_name]["participants"] = original_participants


def test_delete_participant_missing_returns_404():
    # Arrange
    activity_name = "Chess Club"
    missing_email = "missing@mergington.edu"

    # Act
    response = client.delete(
        f"/activities/{activity_name}/participants?email={missing_email}"
    )

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found"
