from django.contrib.auth import models as auth_models
from django.db import models

ROLE_CHOICES = (
    ("applicant", "applicant"),
    ("employer", "employer")
)


class UserManager(auth_models.BaseUserManager):
    def create_user(self, first_name: str, email: str,
                    last_name: str = None, role: str = None,
                    password: str = None,
                    mobile_number: str = None, is_staff=False,
                    is_superuser=False) -> "User":

        if not email:
            raise ValueError("User must have an email")
        if not first_name:
            raise ValueError("User must have first name")

        user = self.model(email=self.normalize_email(email))
        user.first_name = first_name
        user.last_name = last_name
        user.set_password(password)
        user.mobile_number = mobile_number
        user.role = role
        user.is_active = True
        user.is_staff = is_staff
        user.is_superuser = is_superuser

        return user

    def create_superuser(self, first_name: str, last_name: str, email: str, password: str) -> "User":
        user = self.create_user(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password,
            is_staff=True,
            is_superuser=True
        )
        user.save()
        return user


class User(auth_models.AbstractUser):
    first_name = models.CharField(verbose_name="first Name", max_length=50)
    last_name = models.CharField(verbose_name="Last Name", max_length=50, null=True, blank=True)
    username = None
    email = models.EmailField(verbose_name="Email", max_length=255, unique=True)
    password = models.CharField(verbose_name="Password", max_length=255)
    mobile_number = models.CharField(verbose_name="Mobile Number", max_length=20, null=True)
    role = models.CharField(verbose_name="User Role", max_length=20, choices=ROLE_CHOICES,
                            null=True)  # admin and super-user have no role

    object = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]


