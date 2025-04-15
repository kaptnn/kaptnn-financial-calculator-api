import pytest
from sqlalchemy import text

@pytest.mark.parametrize(
    "name, email, password, company_id, expected_status, expected_message",
    [
        (
            "User Test 2",
            "usertest2@gmail.com",
            "Password123!",
            "1e0b4884-0c80-4f49-9942-18b4dd392e14",
            201,
            "User successfully registered"
        ),
        (
            "User Test 1",
            "usertest1@gmail.com",
            "Password123!",
            "1e0b4884-0c80-4f49-9942-18b4dd392e14",
            400,
            "User with this email already exists"
        ),
    ]
)

def test_auth_register_usecases(client, name, email, password, company_id, expected_status, expected_message):
    payload = {
        "name": name,
        "email": email,
        "password": password,
        "company_id": company_id,
    }

    response = client.post("/api/v1/auth/register", json=payload)
    
    assert response.status_code == expected_status, (
        f"For payload {payload}, expected {expected_status} but got {response.status_code}"
    )
    
    data = response.json()

    if expected_status == 201:
        assert "message" in data, "Expected a 'message' key in the response."
        assert data["message"] == expected_message, (
            f"Expected message: '{expected_message}', but got: '{data['message']}'"
        )
    else:
        error_message = data.get("detail") or data.get("message")
        assert error_message is not None, "Expected an error message in the response."
        assert expected_message in error_message, (
            f"Expected error message to contain '{expected_message}', but got '{error_message}'"
        )

@pytest.fixture(scope="function", autouse=True)
def cleanup_user_data(session):
    yield
    test_emails = ["usertest2@gmail.com"]
    session.execute(
        text("DELETE FROM profiles WHERE user_id IN (SELECT id FROM users WHERE email IN :emails)"),
        {'emails': tuple(test_emails)}
    )
    session.execute(
        text("DELETE FROM users WHERE email IN :emails"),
        {'emails': tuple(test_emails)}
    )
    session.commit()
