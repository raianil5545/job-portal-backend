from django.urls import path

import account.views as account_views

urlpatterns = [
    path('register/', account_views.RegisterView.as_view(), name="register"),
    path('login/', account_views.LoginView.as_view(), name="login"),
    path('get-user/', account_views.UserView.as_view(), name="get-user"),
    path('logout/', account_views.LogOutView.as_view(), name="logout")
]