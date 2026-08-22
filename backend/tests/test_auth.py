from app.models.enums import UserRole


def test_login_success(client, make_user):
    make_user("alice@globalcare-demo.com", "Secret123!", UserRole.ADMINISTRATOR)
    response = client.post(
        "/api/v1/auth/login",
        json={"email": "alice@globalcare-demo.com", "password": "Secret123!"},
    )
    assert response.status_code == 200
    body = response.json()
    assert "access_token" in body
    assert "refresh_token" in body
    assert body["token_type"] == "bearer"


def test_login_wrong_password(client, make_user):
    make_user("bob@globalcare-demo.com", "Secret123!", UserRole.ADMINISTRATOR)
    response = client.post(
        "/api/v1/auth/login",
        json={"email": "bob@globalcare-demo.com", "password": "wrong-password"},
    )
    assert response.status_code == 401


def test_login_unknown_email(client):
    response = client.post(
        "/api/v1/auth/login",
        json={"email": "nobody@globalcare-demo.com", "password": "whatever"},
    )
    assert response.status_code == 401


def test_me_requires_token(client):
    response = client.get("/api/v1/auth/me")
    assert response.status_code == 401


def test_me_returns_current_user(client, make_user, auth_header):
    user = make_user("carol@globalcare-demo.com", "Secret123!", UserRole.EXECUTIVE)
    response = client.get("/api/v1/auth/me", headers=auth_header(user))
    assert response.status_code == 200
    body = response.json()
    assert body["email"] == "carol@globalcare-demo.com"
    assert body["role"] == "executive"


def test_refresh_issues_new_access_token(client, make_user):
    make_user("dave@globalcare-demo.com", "Secret123!", UserRole.ADMINISTRATOR)
    login = client.post(
        "/api/v1/auth/login",
        json={"email": "dave@globalcare-demo.com", "password": "Secret123!"},
    ).json()

    response = client.post("/api/v1/auth/refresh", json={"refresh_token": login["refresh_token"]})
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_refresh_rejects_access_token(client, make_user):
    """An access token used as a refresh token must be rejected (type check)."""
    make_user("erin@globalcare-demo.com", "Secret123!", UserRole.ADMINISTRATOR)
    login = client.post(
        "/api/v1/auth/login",
        json={"email": "erin@globalcare-demo.com", "password": "Secret123!"},
    ).json()

    response = client.post("/api/v1/auth/refresh", json={"refresh_token": login["access_token"]})
    assert response.status_code == 401
