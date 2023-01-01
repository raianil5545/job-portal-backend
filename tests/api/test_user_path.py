import pytest


@pytest.mark.django_db
def test_register_user(client):
    payload = dict(
        first_name="applicant",
        last_name="1",
        email="applicant1@gmail.com",
        password="Applicant1@",
        role="applicant",
        mobile_number="7895272100"
    )
    response = client.post("/api/user/register/", payload)
    data = response.data
    assert response.status_code == 200
    assert data["first_name"] == payload["first_name"]
    assert "password" not in data
    assert data["email"] == payload["email"]
    assert data["role"] == payload["role"]


@pytest.mark.django_db
def test_login_user(applicant_registered, client):
    response = client.post("/api/user/login/", {
        "email": "applicant1@gmail.com",
        "password": "Applicant1@"
    })

    assert response.status_code == 200

@pytest.mark.django_db
def test_login_user_fail(applicant_registered, client):
    response = client.post("/api/user/login/", {
        "email": "applicant2@gmail.com",
        "password": "Applicant1@"
    })

    assert response.status_code == 403

@pytest.mark.django_db
def test_logout_user(applicant_auth_client):
    response = applicant_auth_client.post("/api/user/logout/")

    assert response.status_code == 200