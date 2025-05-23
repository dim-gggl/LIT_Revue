from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from authentication.views import SignUpPage, LoggingOutView


urlpatterns = [
    path("", LoginView.as_view(template_name="authentication/login.html"), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("signup/", SignUpPage.as_view(), name="signup"),
]