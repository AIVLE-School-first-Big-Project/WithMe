from django.contrib.auth.views import LogoutView
from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path("login/", views.login, name="Login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("signup/", views.signup, name="signup"),
    path("change_password/", views.change_password, name='change_password'),
    path("change_type/", views.update, name='change_type'),
]
