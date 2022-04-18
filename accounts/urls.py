from django.contrib.auth.views import LoginView
from django.urls import path
from accounts import views


urlpatterns = [
    path("login/", LoginView.as_view(template_name='accounts/login_form.html'), name="Login"),
    path("login_ok/", views.login_ok)
    #path("logout/", views.LogoutView.as_view(), name="logout"),
]