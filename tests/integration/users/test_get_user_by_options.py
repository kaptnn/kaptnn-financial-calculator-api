import pytest

@pytest.mark.parametrize("option_type, param_key", [
    ("id", "id"),
    ("email", "email"),
    ("company", "company_id"),
])

def test_get_user_by_options_usecase(client, option_type, param_key):
    login_payload = {"email": "usertest1@gmail.com", "password": "Password123!"}
    login_response = client.post("/api/v1/auth/login", json=login_payload)
    assert login_response.status_code == 200

    access_token = login_response.cookies.get("access_token")
    assert access_token, "Access token not set"
    
    headers = {"Authorization": f"Bearer {access_token}"}

    user_response = client.get("/api/v1/users/me", headers=headers)

    user_info = user_response.json()["result"]

    value = user_info[param_key]
    
    response = client.get(f"/api/v1/users/user/{option_type}/{value}/", headers=headers)
    assert response.status_code == 200
    result = response.json()["result"]

    if option_type == "company":
        assert isinstance(result, list)
    else:
        assert isinstance(result, dict)