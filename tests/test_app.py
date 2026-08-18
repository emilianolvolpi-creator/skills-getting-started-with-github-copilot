from fastapi.testclient import TestClient

from src.app import app, activities


client = TestClient(app)


def reset_participants():
    activities["Chess Club"]["participants"] = [
        "michael@mergington.edu",
        "daniel@mergington.edu",
    ]
    activities["Programming Class"]["participants"] = [
        "emma@mergington.edu",
        "sophia@mergington.edu",
    ]
    activities["Gym Class"]["participants"] = [
        "john@mergington.edu",
        "olivia@mergington.edu",
    ]

    for activity_name in [
        "Basketball Team",
        "Swimming Club",
        "Art Studio",
        "Drama Club",
        "Debate Team",
        "Science Club",
    ]:
        activities[activity_name]["participants"] = []


def test_get_activities_returns_activity_catalog():
    # Arrange
    reset_participants()

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert "Programming Class" in data
    assert "Gym Class" in data
    assert len(data) >= 9


def test_signup_adds_participant_to_activity():
    # Arrange
    reset_participants()
    email = "test.student@mergington.edu"

    # Act
    response = client.post(
        "/activities/Chess Club/signup",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 200
    assert email in activities["Chess Club"]["participants"]
    assert response.json()["message"] == f"Signed up {email} for Chess Club"


def test_signup_prevents_duplicate_participant():
    # Arrange
    reset_participants()
    email = "michael@mergington.edu"

    # Act
    response = client.post(
        "/activities/Chess Club/signup",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student is already signed up"


def test_signup_invalid_activity_returns_404():
    # Arrange
    reset_participants()

    # Act
    response = client.post(
        "/activities/Invalid Activity/signup",
        params={"email": "student@mergington.edu"},
    )

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_removes_participant_from_activity():
    # Arrange
    reset_participants()
    email = "michael@mergington.edu"

    # Act
    response = client.delete(
        "/activities/Chess Club/unregister",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 200
    assert email not in activities["Chess Club"]["participants"]
    assert response.json()["message"] == f"Unregistered {email} from Chess Club"


def test_unregister_missing_participant_returns_400():
    # Arrange
    reset_participants()
    email = "missing.student@mergington.edu"

    # Act
    response = client.delete(
        "/activities/Chess Club/unregister",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student is not signed up for this activity"


def test_unregister_invalid_activity_returns_404():
    # Arrange
    reset_participants()

    # Act
    response = client.delete(
        "/activities/Invalid Activity/unregister",
        params={"email": "student@mergington.edu"},
    )

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
