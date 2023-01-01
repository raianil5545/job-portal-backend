import pytest
from PIL import Image
import tempfile
from django.core.files.uploadedfile import SimpleUploadedFile
from account import services as user_services
from rest_framework.test import APIClient


new_client = APIClient()


@pytest.mark.django_db
def test_employer_profile_created(employer_auth_client, employer_registered):
    image = Image.new('RGBA', size=(50, 50), color=(155, 0, 0))
    file = tempfile.NamedTemporaryFile(suffix='.png')
    image.save(file)
    small_gif = (
        b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04'
        b'\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02'
        b'\x02\x4c\x01\x00\x3b'
    )
    uploaded = SimpleUploadedFile('small.gif', small_gif, content_type='image/gif')
    with open(file.name, 'rb') as data:
        payload = dict(
            user=employer_registered.id,
            founded_year="1990-04-12",
            website_url="www.employer1.com",
            logo=data,
            street_address="kupondal",
            city="kathmandu",
            province="bagmati",
            locations="kathmandu, pokhara",
            cover_page=uploaded
        )
        response = employer_auth_client.post("/api/employer/profile/", payload, format='multipart')
    assert response.status_code == 201

@pytest.mark.django_db
def test_get_employer_profile_correct_employer(employer_auth_client, employer_profile_created):

    response = employer_auth_client.get("/api/employer/profile/")
    assert response.status_code == 200

@pytest.mark.django_db
def test_get_employer_profile_incorrect_employer(employer_profile_created):
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

    response = new_client.get(f"/api/employer/profile/")
    assert response.status_code == 403

@pytest.mark.django_db
def test_get_employer_profile_incorrect_employer_id(employer_profile_created, client):
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
    profile_id = employer_profile_created["id"]

    response = new_client.get(f"/api/employer/profile/{profile_id}/")
    assert response.status_code == 403


@pytest.mark.django_db
def test_update_employer_profile(employer_profile_created, employer_auth_client):
    profile_id = employer_profile_created["id"]

    response = employer_auth_client.patch(f"/api/employer/profile/{profile_id}/", {"website": "www.newemployer1.com"})
    assert response.status_code == 200

@pytest.mark.django_db
def test_update_employer_profile_invalid_employer(employer_profile_created):
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
    profile_id = employer_profile_created["id"]

    response = new_client.patch(f"/api/employer/profile/{profile_id}/", {"website": "www.newemployer1.com"})
    assert response.status_code == 403
