import pytest

@pytest.mark.parametrize("email, password, expect_success", [
    ("usertest1@gmail.com", "Password123!", True),
    ("invaliduser@gmail.com", "Password123!", False),
    ("usertest1@gmail.com", "WrongPassword!", False),
])
def test_get_current_user_usecases(client, email, password, expect_success):
    login_payload = {
        "email": email,
        "password": password,
    }

    login_response = client.post("/api/v1/auth/login", json=login_payload)

    if expect_success:
        assert login_response.status_code == 200, f"Login failed for valid user: {email}"

        access_token = login_response.cookies.get("access_token")
        assert access_token, "Access token not set after login"

        headers = {
            "Authorization": f"Bearer {access_token}"
        }

        response = client.get("/api/v1/users/me", headers=headers)
        assert response.status_code == 200, "Expected 200 OK from /me endpoint"

        data = response.json()
        assert "message" in data
        assert data["message"].lower() == "user retrieved successfully"
        assert "result" in data
        assert isinstance(data["result"], dict), "Expected user data to be a dict"

        result = data["result"]
        assert "id" in result
        assert "email" in result
        assert result["email"] == email
        assert result.get("password") is None, "Password should not be exposed"
    else:
        assert login_response.status_code in (401, 400)

        response = client.get("/api/v1/users/me")
        assert response.status_code in (401, 403), \
            "Unauthorized user should not access /me"
