import pytest
from PIL import Image
import tempfile
from account import services as user_services
from rest_framework.test import APIClient


new_client = APIClient()


@pytest.mark.django_db
def test_create_applicant_profile(applicant_registered, applicant_auth_client):
    image = Image.new('RGBA', size=(50, 50), color=(155, 0, 0))
    file = tempfile.NamedTemporaryFile(suffix='.png')
    image.save(file)
    with open(file.name, 'rb') as data:
        payload = dict(
            user=applicant_registered.id,
            level="entry level",
            skills="python, react",
            experience=2,
            date_of_birth="1990-03-13",
            gender="male",
            profile_pic=data,
            expected_salary=50000,
            street="kupondal",
            city="kathmandu",
            province="bagmati",
            preferred_job_location="kathmandu"
        )
        response = applicant_auth_client.post("/api/applicant/profile/", payload, format='multipart')
    assert response.status_code == 201
    assert response.data["user"] == applicant_registered.id


@pytest.mark.django_db
def test_create_applicant_profile_with_wrong_credentials_role(employer_auth_client, employer_registered):
    image = Image.new('RGBA', size=(50, 50), color=(155, 0, 0))
    file = tempfile.NamedTemporaryFile(suffix='.png')
    image.save(file)
    with open(file.name, 'rb') as data:
        payload = dict(
            user=employer_registered.id,
            level="entry level",
            skills="python, react",
            experience=2,
            date_of_birth="1990-03-13",
            gender="male",
            profile_pic=data,
            expected_salary=50000,
            street="kupondal",
            city="kathmandu",
            province="bagmati",
            preferred_job_location="kathmandu"
        )
        response = employer_auth_client.post("/api/applicant/profile/", payload, format='multipart')
    assert response.status_code == 403


@pytest.mark.django_db
def test_get_applicant_profile(applicant_auth_client, applicant_profile_created):
    response = applicant_auth_client.get("/api/applicant/profile/")
    assert response.status_code == 200
    assert len(response.data) == len(applicant_profile_created)
    assert response.data["user"] == applicant_profile_created["user"]


@pytest.mark.django_db
def test_get_applicant_profile_fail(employer_auth_client):
    response = employer_auth_client.get("/api/applicant/profile/")
    assert response.status_code == 403


@pytest.mark.django_db
def test_get_applicant_profile_by_id(applicant_auth_client, applicant_profile_created):
    profile_id = applicant_profile_created["id"]
    response = applicant_auth_client.get(f"/api/applicant/profile/{profile_id}/")
    assert response.status_code == 200


@pytest.mark.django_db
def test_get_applicant_profile_by_id_wrong_applicant_forbidden(applicant_profile_created):
    user_dc = user_services.UserDataClass(
        first_name="applicant",
        last_name="2",
        email="applicant2@gmail.com",
        password="Applicant2@",
        role="applicant",
        mobile_number="7892457909"
    )
    user = user_services.create_user(user_dc)
    new_client.post("/api/user/login/", {
        "email": "applicant2@gmail.com",
        "password": "Applicant2@"
    })
    profile_id = applicant_profile_created["id"]
    response = new_client.get(f"/api/applicant/profile/{profile_id}/")
    assert response.status_code == 403


@pytest.mark.django_db
def test_update_applicant_profile(applicant_auth_client, applicant_profile_created):
    profile_id = applicant_profile_created["id"]
    response = applicant_auth_client.patch(f"/api/applicant/profile/{profile_id}/", data={"level": "mid level"})
    assert response.status_code == 200
    assert response.data["level"] == "mid level"

@pytest.mark.django_db
def test_update_applicant_profile_by_wrong_applicant_forbidden(applicant_profile_created):
    user_dc = user_services.UserDataClass(
        first_name="applicant",
        last_name="2",
        email="applicant2@gmail.com",
        password="Applicant2@",
        role="applicant",
        mobile_number="7892457909"
    )
    user = user_services.create_user(user_dc)
    new_client.post("/api/user/login/", {
        "email": "applicant2@gmail.com",
        "password": "Applicant2@"
    })
    profile_id = applicant_profile_created["id"]
    response = new_client.patch(f"/api/applicant/profile/{profile_id}/", data={"level": "mid level"})
    assert response.status_code == 403# forbidden status code
