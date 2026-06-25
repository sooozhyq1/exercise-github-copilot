ACTIVITY_NAME = "Chess Club"


def test_get_activities(client):
    # Arrange
    expected_key = ACTIVITY_NAME

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert expected_key in data
    assert "participants" in data[expected_key]


def test_signup_success(client):
    # Arrange
    email = "newstudent@mergington.edu"

    # Act
    response = client.post(
        f"/activities/{ACTIVITY_NAME}/signup",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 200
    assert response.json() == {
        "message": f"Signed up {email} for {ACTIVITY_NAME}"
    }

    follow_up = client.get("/activities")
    assert email in follow_up.json()[ACTIVITY_NAME]["participants"]


def test_signup_duplicate_returns_400(client):
    # Arrange
    email = "michael@mergington.edu"

    # Act
    response = client.post(
        f"/activities/{ACTIVITY_NAME}/signup",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student is already signed up for this activity"


def test_signup_unknown_activity_returns_404(client):
    # Arrange
    unknown_activity = "Science Club"
    email = "student@mergington.edu"

    # Act
    response = client.post(
        f"/activities/{unknown_activity}/signup",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
