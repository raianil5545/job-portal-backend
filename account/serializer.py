from rest_framework import serializers
from . import services
from . import customvalidators


class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, validators=[customvalidators.PasswordValidator()])
    role = serializers.CharField(validators=[customvalidators.RoleValidator()])
    mobile_number = serializers.CharField()

    def to_internal_value(self, data):
        data = super().to_internal_value(data)
        return services.UserDataClass(**data)


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(validators=[customvalidators.PasswordValidator()])
