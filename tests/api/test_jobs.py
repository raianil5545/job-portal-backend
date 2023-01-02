import pytest
from rest_framework.test import APIClient
from account import services as user_services

new_client = APIClient()


@pytest.mark.django_db
def test_create_job_by_employer_pass(employer_auth_client, employer_profile_created, job_payload):
    response = employer_auth_client.post("/api/jobs/", job_payload)
    assert response.status_code == 201
    assert len(response.data) == len(job_payload) + 1 #for added id field in db
    assert response.data["job_name"] == job_payload["job_name"]


@pytest.mark.django_db
def test_create_job_by_applicant_forbidden(applicant_registered, employer_profile_created, job_payload):
    new_client.post("/api/user/login/", {
        "email": "applicant1@gmail.com",
        "password": "Applicant1@"
    })
    response = new_client.post("/api/jobs/", job_payload)
    assert response.status_code == 403


@pytest.mark.django_db
def test_get_jobs_with_employer_credentials(employer_auth_client, job_payload):
    employer_auth_client.post("/api/jobs/", job_payload)
    response = employer_auth_client.get("/api/jobs/")
    assert response.status_code == 200
    assert len(response.data) == 1


@pytest.mark.django_db
def test_get_jobs_with_applicant_credentials_allow(employer_auth_client, job_payload):
    employer_auth_client.post("/api/jobs/", job_payload)
    new_client.post("/api/user/login/", {
        "email": "applicant1@gmail.com",
        "password": "Applicant1@"
    })
    response = new_client.get("/api/jobs/")
    assert response.status_code == 200
    assert len(response.data) == 1


@pytest.mark.django_db
def test_get_jobs_with_no_credentials_allow(employer_auth_client, job_payload):
    employer_auth_client.post("/api/jobs/", job_payload)
    response = new_client.get("/api/jobs/")
    assert response.status_code == 200
    assert len(response.data) == 1


@pytest.mark.django_db
def test_get_job_with_id_correct_employer_credentials(employer_auth_client, job_payload):
    job_created_res = employer_auth_client.post("/api/jobs/", job_payload)
    job_id = job_created_res.data["id"]
    response = employer_auth_client.get(f"/api/jobs/{job_id}/")
    assert response.status_code == 200
    assert len(response.data) == len(job_payload) + 5 # id and other fields retrieved from custom view
    assert "is_active" in response.data
    assert "employer_logo" in response.data


@pytest.mark.django_db
def test_get_job_with_id_with_incorrect_credentials_pass(employer_auth_client, job_payload):
    job_created_res = employer_auth_client.post("/api/jobs/", job_payload)
    job_id = job_created_res.data["id"]
    new_client.post("/api/user/login/", {
        "email": "applicant1@gmail.com",
        "password": "Applicant1@"
    })
    response = new_client.get(f"/api/jobs/{job_id}/")
    assert response.status_code == 200
    assert "is_active" in response.data
    assert "employer_logo" in response.data

@pytest.mark.django_db
def test_update_job_with_correct_credentials_pass(employer_auth_client, job_payload):
    job_created_res = employer_auth_client.post("/api/jobs/", job_payload)
    job_id = job_created_res.data["id"]
    response = employer_auth_client.patch(f"/api/jobs/{job_id}/", {"job_name": "new name"})
    assert response.status_code == 200
    assert response.data["job_name"] == "new name"

@pytest.mark.django_db
def test_update_job_with_incorrect_credentials_403(employer_auth_client, job_payload):
    job_created_res = employer_auth_client.post("/api/jobs/", job_payload)
    job_id = job_created_res.data["id"]
    user_dc = user_services.UserDataClass(
        first_name="employer",
        last_name="2",
        email="employer2@gmail.com",
        password="Employer2@",
        role="employer",
        mobile_number="7892457909"
    )
    new_client.post("/api/user/login/", {
        "email": "employer2@gmail.com",
        "password": "Employer2@"
    })
    response = new_client.patch(f"/api/jobs/{job_id}/", {"job_name": "new name"})
    assert response.status_code == 403


