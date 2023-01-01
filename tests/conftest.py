import pytest
from account import services as user_services
from rest_framework.test import APIClient
from PIL import Image
import tempfile
from django.core.files.uploadedfile import SimpleUploadedFile



@pytest.fixture
def applicant_registered():
    user_dc = user_services.UserDataClass(
        first_name="applicant1",
        last_name="1",
        email="applicant1@gmail.com",
        password="Applicant1@",
        role="applicant",
        mobile_number="7892457909"
    )
    user = user_services.create_user(user_dc)
    return user


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def applicant_auth_client(applicant_registered, client):
    client.post("/api/user/login/", {
        "email": "applicant1@gmail.com",
        "password": "Applicant1@"
    })
    return client


@pytest.fixture
def applicant_profile_created(applicant_auth_client, applicant_registered):
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
    return response.data


@pytest.fixture
def employer_registered():
    user_dc = user_services.UserDataClass(
        first_name="employer1",
        last_name="1",
        email="employer1@gmail.com",
        password="Employer1@",
        role="employer",
        mobile_number="7892457909"
    )
    return user_services.create_user(user_dc)


@pytest.fixture
def employer_auth_client(employer_registered, client):
    client.post("/api/user/login/", {
        "email": "employer1@gmail.com",
        "password": "Employer1@"
    })
    return client

@pytest.fixture
def employer_profile_created(employer_auth_client, employer_registered):
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
        return response.data

