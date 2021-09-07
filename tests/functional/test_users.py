def test_get_login_page(test_client):
    response = test_client.get("/login")
    assert response.status_code == 200
    assert b"Login" in response.data
    assert b"Email" in response.data
    assert b"Password" in response.data


def test_invalid_login(test_client, register_user):
    response = test_client.post(
        "/login",
        data={
            "email": "unknown@email.com",
            "password": "NotInHere",
        },
    )
    assert response.status_code == 200
    assert b"ERROR! Incorrect login credentials." in response.data


def test_valid_login(test_client, register_user):
    response = test_client.post(
        "/login",
        data={
            "email": "hire@me.com",
            "password": "TestUser123",
        },
        follow_redirects=True,
    )
    assert response.status_code == 200


def test_valid_login(test_client, register_user):
    response = test_client.post(
        "/login",
        data={
            "email": "hire@me.com",
            "password": "TestUser123",
        },
        follow_redirects=True,
    )
    assert response.status_code == 200


def test_valid_login_and_logout(test_client, register_user):
    # Login
    response = test_client.post(
        "/login",
        data={
            "email": "hire@me.com",
            "password": "TestUser123",
        },
        follow_redirects=True,
    )
    assert response.status_code == 200

    # Logout
    response = test_client.get("/logout", follow_redirects=True)
    assert response.status_code == 200
