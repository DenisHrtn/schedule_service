from django.urls import path
from rest_framework import routers

from users.views.logout import LogoutView
from users.views.registration import RegistrationAPIView
from users.views.login import LoginView

router = routers.DefaultRouter()

urlpatterns = [
    path('register/', RegistrationAPIView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]