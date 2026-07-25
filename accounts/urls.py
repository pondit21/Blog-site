
from django.urls import path
from accounts.views import RegistrationView

from django.contrib.auth.views import (
    LoginView,
    LogoutView,
)

urlpatterns = [
    path(
        'register/',
        RegistrationView.as_view(),
        name='register'
    ),

    path(
        'login/',
        LoginView.as_view(
            template_name='registration/login.html'
        ),
        name='login'
    ),

    path(
        'logout/',
        LogoutView.as_view(next_page='login'),
        name='logout'
    ),
]
