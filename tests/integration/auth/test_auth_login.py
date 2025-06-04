import pytest

@pytest.mark.parametrize("email, password, expected_status, expect_tokens", [
    ("usertest1@gmail.com", "Password123!", 200, True),
    ("usertest1@gmail.com", "WrongPassword123!", 401, False),
    ("bocilnotexist@gmail.com", "Password123!", 401, False),
])

def test_auth_login_usecases(client, email, password, expected_status, expect_tokens):
    payload = {"email": email, "password": password}
    response = client.post("/api/v1/auth/login", json=payload)
    
    assert response.status_code == expected_status, (
        f"Expected status {expected_status} but got {response.status_code} for email '{email}'"
    )
    
    data = response.json()
    
    if expect_tokens:
        assert "message" in data, "Response JSON should contain a 'message' key."
        assert data["message"] == "User successfully logged in", "Unexpected success message."
        
        assert "result" in data, "Response JSON should contain a 'result' key."
        tokens = data["result"]
        
        assert tokens.get("token_type") == "Bearer", "Token type should be 'Bearer'."
        assert isinstance(tokens.get("access_token"), str) and tokens.get("access_token"), \
            "Access token should be a non-empty string."
        assert isinstance(tokens.get("refresh_token"), str) and tokens.get("refresh_token"), \
            "Refresh token should be a non-empty string."
        
        cookies = response.cookies
        assert "access_token" in cookies, "Response cookies should contain 'access_token'."
        assert "refresh_token" in cookies, "Response cookies should contain 'refresh_token'."
    else:
        assert "detail" in data, "Error responses should contain a 'detail' key."
