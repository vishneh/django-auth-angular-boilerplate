from rest_framework.authtoken.views import obtain_auth_token
from django.urls import path

from account.views import (
    UserRegistrationView,
    ForgotPasswordView,
    ResetPasswordView,
)


urlpatterns = [
    path('login/', obtain_auth_token),
    path('createuser/', UserRegistrationView),
    path('forgotpassword/', ForgotPasswordView),
    path('resetpassword/', ResetPasswordView),

]