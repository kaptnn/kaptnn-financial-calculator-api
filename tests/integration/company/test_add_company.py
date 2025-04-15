import pytest
from sqlalchemy import text
@pytest.fixture
def auth_token(client):
    login_payload = {"email": "usertest1@gmail.com", "password": "Password123!"}
    login_response = client.post("/api/v1/auth/login", json=login_payload)
    assert login_response.status_code == 200
    access_token = login_response.cookies.get("access_token")
    return access_token

@pytest.mark.parametrize(
    "company_name, year_of_assignment, start_audit_period, end_audit_period, expected_status, expected_message",
    [
        (
            "Example Company Test 1",
            2024,
            "2024-07-16",
            "2025-07-16",
            201,
            "Company successfully registered"
        ),
        (
            "",
            2024,
            "2024-07-16",
            "2025-07-16",
            422,
            "company_name"
        ),
        (
            "Example Company Test 2",
            -1, 
            "2024-07-16",
            "2025-07-16",
            422,
            "year_of_assignment"
        ),
    ]
)

def test_add_company_usecases(
    client,
    auth_token,
    company_name,
    year_of_assignment,
    start_audit_period,
    end_audit_period,
    expected_status,
    expected_message,
):
    payload = {
        "company_name": company_name,
        "year_of_assignment": year_of_assignment,
        "start_audit_period": start_audit_period,
        "end_audit_period": end_audit_period,
    }

    headers = {"Authorization": f"Bearer {auth_token}"}
    response = client.post("/api/v1/companies/", json=payload, headers=headers)
    
    assert response.status_code == expected_status, (
        f"For payload {payload}, expected status {expected_status} but got {response.status_code}"
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
        assert expected_message in str(error_message), (
            f"Expected error message to contain '{expected_message}', but got '{error_message}'"
        )

@pytest.fixture(scope="function", autouse=True)
def cleanup_company_data(session):
    yield
    test_company_names = ("Example Company Test 1", "Example Company Test 2")
    session.execute(
        text("DELETE FROM companies WHERE company_name IN :names"),
        {'names': test_company_names}
    )
    session.commit()
