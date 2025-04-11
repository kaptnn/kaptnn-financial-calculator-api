import pytest

@pytest.mark.parametrize("email, password, expect_success", [
    ("usertest1@gmail.com", "Password123!", True),
    ("invaliduser@gmail.com", "Password123!", False),
    ("usertest1@gmail.com", "WrongPassword!", False),
])

def test_get_all_users_usecases(client, email, password, expect_success):
    login_payload = {
        "email": email,
        "password": password,
    }

    login_response = client.post("/api/v1/auth/login", json=login_payload)

    if expect_success:
        assert login_response.status_code == 200, f"Login failed for valid user: {email}"
        access_token = login_response.cookies.get("access_token")
        assert access_token is not None, "Access token not set after login"

        headers = {
            "Authorization": f"Bearer {access_token}"
        }

        response = client.get("/api/v1/users/", headers=headers)
        assert response.status_code == 200, "Expected successful user fetch"
        
        data = response.json()
        assert "result" in data
        assert "pagination" in data
        assert isinstance(data["result"], list)
    else:
        assert login_response.status_code == 401 or login_response.status_code == 400

        response = client.get("/api/v1/users/")
        assert response.status_code == 401 or response.status_code == 403, \
            "Unauthorized access should be denied"
