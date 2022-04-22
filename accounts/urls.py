from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path("login/", LoginView.as_view(template_name='accounts/login_form.html'), name="Login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("login_ok/", views.login_ok),
    path("signup/", views.signup, name="signup"),
    path("change_password/", views.change_password, name='change_password'),
    path("change_type/", views.update, name='change_type'),
]