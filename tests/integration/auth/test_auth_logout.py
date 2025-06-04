def test_auth_logout(client):
    login_payload = {
        "email": "usertest1@gmail.com",
        "password": "Password123!",
    }

    login_response = client.post("/api/v1/auth/login", json=login_payload)
    assert login_response.status_code == 200, "Login failed before logout test."

    access_token = login_response.cookies["access_token"]
    refresh_token = login_response.cookies["refresh_token"]

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    logout_response = client.post("/api/v1/auth/logout", headers=headers)

    assert logout_response.status_code == 200
    data = logout_response.json()
    assert "message" in data
    assert data["message"].lower() == "logged out"

    set_cookie_headers = logout_response.headers.get_list("set-cookie")

    def cookie_is_deleted(cookie_header, cookie_name):
        cookie = cookie_header.lower()
        return (
            cookie_name in cookie and
            ("max-age=0" in cookie or "expires=thu, 01 jan 1970" in cookie)
        )

    assert any(cookie_is_deleted(header, "access_token") for header in set_cookie_headers), \
        "Access token cookie was not cleared."

    assert any(cookie_is_deleted(header, "refresh_token") for header in set_cookie_headers), \
        "Refresh token cookie was not cleared."
