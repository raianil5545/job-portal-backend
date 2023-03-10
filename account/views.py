from rest_framework.views import APIView
from rest_framework import views, response, exceptions, permissions, status

from . import serializer as user_serializer
from . import services
from . import authentication


class RegisterView(APIView):
    def post(self, request):
        user = services.user_email_selector(email=request.data["email"])
        if user:
            return response.Response(data=f"{user.email} already exist", status=status.HTTP_400_BAD_REQUEST)
        serializer = user_serializer.UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        serializer.instance = services.create_user(user_dc=data)
        return response.Response(data=serializer.data)


class LoginView(views.APIView):
    def post(self, request):
        serializer = user_serializer.LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.data
        email = data["email"]
        password = data["password"]

        user = services.user_email_selector(email=email)
        if user is None:
            raise exceptions.AuthenticationFailed("Invalid Credentials")
        if not user.check_password(raw_password=password):
            raise exceptions.AuthenticationFailed("Invalid Credentials")
        token = services.create_token(user_id=user.id)
        resp = response.Response()
        resp.set_cookie(key="job_portal_jwt", value=token, httponly=True)
        return resp


class UserView(APIView):
    authentication_classes = (authentication.CustomUserAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        user = request.user
        serializer = user_serializer.UserSerializer(user)
        return response.Response(data=serializer.data)


class LogOutView(views.APIView):
    authentication_classes = (authentication.CustomUserAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        resp = response.Response()
        resp.delete_cookie("job_portal_jwt")
        resp.data = {"msg": "logged out successfully"}
        return resp
