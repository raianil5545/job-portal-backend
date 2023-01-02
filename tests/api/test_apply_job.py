import pytest
from rest_framework.test import APIClient
from account import services as user_services

new_client = APIClient()


@pytest.mark.django_db
def test_apply_job_with_applicant_credentials(job_payload, employer_auth_client, applicant_registered):
    response_job = employer_auth_client.post("/api/jobs/", job_payload)
    apply_job_payload = dict(
        user=applicant_registered.id,
        job=response_job.data["id"],
        job_name=response_job.data["job_name"]
    )
    new_client.post("/api/user/login/", {
        "email": "applicant1@gmail.com",
        "password": "Applicant1@"
    })
    response = new_client.post("/api/job-posted/", apply_job_payload)
    assert response.status_code == 201
    assert len(response.data) == 3
    assert response.data["job_name"] == response_job.data["job_name"]


@pytest.mark.django_db
def test_apply_job_with_employer_credentials_forbidden(job_payload, employer_auth_client, employer_registered):
    response_job = employer_auth_client.post("/api/jobs/", job_payload)
    apply_job_payload = dict(
        user=employer_registered.id,
        job=response_job.data["id"],
        job_name=response_job.data["job_name"]
    )
    response = employer_auth_client.post("/api/job-posted/", apply_job_payload)
    assert response.status_code == 403


@pytest.mark.django_db
def test_get_apply_job_with_applicant_credentials(job_payload, employer_auth_client, applicant_registered):
    response_job = employer_auth_client.post("/api/jobs/", job_payload)
    apply_job_payload = dict(
        user=applicant_registered.id,
        job=response_job.data["id"],
        job_name=response_job.data["job_name"]
    )
    new_client.post("/api/user/login/", {
        "email": "applicant1@gmail.com",
        "password": "Applicant1@"
    })
    new_client.post("/api/job-posted/", apply_job_payload)
    response = new_client.get("/api/job-posted/", apply_job_payload)
    assert response.status_code == 200
    assert len(response.data) == 1  # return list of 1 job as json obj
    assert response.data[0]["job_name"] == response_job.data["job_name"]


@pytest.mark.django_db
def test_get_apply_job_with_employer_credentials_forbidden(job_payload, employer_auth_client, applicant_registered):
    response_job = employer_auth_client.post("/api/jobs/", job_payload)
    apply_job_payload = dict(
        user=applicant_registered.id,
        job=response_job.data["id"],
        job_name=response_job.data["job_name"]
    )
    new_client.post("/api/user/login/", {
        "email": "applicant1@gmail.com",
        "password": "Applicant1@"
    })
    new_client.post("/api/job-posted/", apply_job_payload)
    response = employer_auth_client.get("/api/job-posted/", apply_job_payload)
    assert response.status_code == 403


@pytest.mark.django_db
def test_get_apply_job_id_with_incorrect_applicant_credentials_forbidden(job_payload, employer_auth_client,
                                                                         applicant_registered):
    response_job = employer_auth_client.post("/api/jobs/", job_payload)
    apply_job_payload = dict(
        user=applicant_registered.id,
        job=response_job.data["id"],
        job_name=response_job.data["job_name"]
    )
    app_1_client = APIClient()
    app_1_client.post("/api/user/login/", {
        "email": "applicant1@gmail.com",
        "password": "Applicant1@"
    })

    app_1_client.post("/api/job-posted/", apply_job_payload)
    apply_job = app_1_client.get("/api/job-posted/")
    apply_job_id = apply_job.data[0]["id"]
    user_dc = user_services.UserDataClass(
        first_name="applicant",
        last_name="2",
        email="applicant2@gmail.com",
        password="Applicant2@",
        role="applicant",
        mobile_number="7892457099"
    )
    user = user_services.create_user(user_dc)
    applicant2_client = APIClient()
    resp = applicant2_client.post("/api/user/login/", {
        "email": "applicant2@gmail.com",
        "password": "Applicant2@"
    })
    response = applicant2_client.get(f"/api/job-posted/{apply_job_id}/")
    assert response.status_code == 403


@pytest.mark.django_db
def test_get_apply_job_id_with_correct_applicant_credentials_forbidden(job_payload, employer_auth_client,
                                                                       applicant_registered):
    response_job = employer_auth_client.post("/api/jobs/", job_payload)
    apply_job_payload = dict(
        user=applicant_registered.id,
        job=response_job.data["id"],
        job_name=response_job.data["job_name"]
    )
    app_1_client = APIClient()
    app_1_client.post("/api/user/login/", {
        "email": "applicant1@gmail.com",
        "password": "Applicant1@"
    })

    app_1_client.post("/api/job-posted/", apply_job_payload)
    apply_job = app_1_client.get("/api/job-posted/")
    apply_job_id = apply_job.data[0]["id"]
    response = app_1_client.get(f"/api/job-posted/{apply_job_id}/")
    assert response.status_code == 200


@pytest.mark.django_db
def test_update_apply_job_id_with_correct_applicant_credentials_forbidden(job_payload, employer_auth_client,
                                                                          applicant_registered):
    response_job = employer_auth_client.post("/api/jobs/", job_payload)
    apply_job_payload = dict(
        user=applicant_registered.id,
        job=response_job.data["id"],
        job_name=response_job.data["job_name"]
    )
    app_1_client = APIClient()
    app_1_client.post("/api/user/login/", {
        "email": "applicant1@gmail.com",
        "password": "Applicant1@"
    })

    app_1_client.post("/api/job-posted/", apply_job_payload)
    apply_job = app_1_client.get("/api/job-posted/")
    apply_job_id = apply_job.data[0]["id"]
    response = app_1_client.patch(f"/api/job-posted/{apply_job_id}/", {"job_name": "new name some"})
    assert response.status_code == 200
    assert response.data["job_name"] == "new name some"

@pytest.mark.django_db
def test_upodate_apply_job_id_with_incorrect_applicant_credentials_forbidden(job_payload, employer_auth_client,
                                                                         applicant_registered):
    response_job = employer_auth_client.post("/api/jobs/", job_payload)
    apply_job_payload = dict(
        user=applicant_registered.id,
        job=response_job.data["id"],
        job_name=response_job.data["job_name"]
    )
    app_1_client = APIClient()
    app_1_client.post("/api/user/login/", {
        "email": "applicant1@gmail.com",
        "password": "Applicant1@"
    })

    app_1_client.post("/api/job-posted/", apply_job_payload)
    apply_job = app_1_client.get("/api/job-posted/")
    apply_job_id = apply_job.data[0]["id"]
    user_dc = user_services.UserDataClass(
        first_name="applicant",
        last_name="2",
        email="applicant2@gmail.com",
        password="Applicant2@",
        role="applicant",
        mobile_number="7892457099"
    )
    user = user_services.create_user(user_dc)
    applicant2_client = APIClient()
    resp = applicant2_client.post("/api/user/login/", {
        "email": "applicant2@gmail.com",
        "password": "Applicant2@"
    })
    response = applicant2_client.patch(f"/api/job-posted/{apply_job_id}/")
    assert response.status_code == 403
