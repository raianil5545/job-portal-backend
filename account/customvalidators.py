import re
from rest_framework import serializers


class RoleValidator:
    def __call__(self, value):
        if value not in ["applicant", "employer"]:
            message = 'applicant or applicant, employer only allowed in role'
            raise serializers.ValidationError(message)

class PasswordValidator:
    def __call__(self, value):
        pattern = r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$"
        result = re.findall(pattern, value)
        if result:
            return value
        else:
            raise serializers.ValidationError("Minimum 8 characters, at least one upper case, one lower and number")
