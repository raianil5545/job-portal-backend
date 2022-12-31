import jwt
from typing import TYPE_CHECKING
import dataclasses
from django.conf import settings
import datetime

from . models import User


if TYPE_CHECKING:
    from models import User

@dataclasses.dataclass
class UserDataClass:
    first_name: str
    last_name: str
    email: str
    role: str
    mobile_number: str
    id: int = None
    password: str = None

    @classmethod
    def from_instance(cls, user: "User") -> "UserDataClass":
        return cls(
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            id=user.id,
            role=user.role,
            mobile_number=user.mobile_number
        )


def create_user(user_dc: "UserDataClass") -> "UserDataClass":
    instance = User(
        first_name=user_dc.first_name,
        last_name=user_dc.last_name,
        email=user_dc.email,
        role=user_dc.role
    )
    if user_dc.password is not None:
        instance.set_password(user_dc.password)
    if user_dc.mobile_number:
        instance.mobile_number = user_dc.mobile_number

    instance.save()
    return UserDataClass.from_instance(instance)


def user_email_selector(email: str) -> "UserDataClass":
    user = User.objects.filter(email=email).first()
    return user


def create_token(user_id: int) -> str:
    payload = dict(
        id=user_id,
        exp=datetime.datetime.now() + datetime.timedelta(hours=24),
        iat=datetime.datetime.utcnow()
    )
    token = jwt.encode(payload, settings.JWT_SECRET, algorithm="HS256")
    return token