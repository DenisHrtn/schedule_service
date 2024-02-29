from django.urls import path
from rest_framework import routers

from users.views.change_password import ChangePasswordView
from users.views.forgot_password import ForgotPasswordView
from users.views.logout import LogoutView
from users.views.registration import RegistrationAPIView
from users.views.login import LoginView
from users.views.confirmation_register import ConfirmationRegisterView
from users.views.users import UserViewSet
from users.views.profile import ProfileViewSet

router = routers.DefaultRouter()
router.register('users', UserViewSet, basename='users')
router.register('profile', ProfileViewSet, basename='profile')

urlpatterns = [
    path('register/', RegistrationAPIView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('users/confirmation-register/', ConfirmationRegisterView.as_view(), name='confirmation-register'),
    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot-password'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
] + router.urls