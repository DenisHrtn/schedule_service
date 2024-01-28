from django.urls import path
from rest_framework import routers

from users.views.registration import RegistrationAPIView

router = routers.DefaultRouter()

urlpatterns = [
    path('register/', RegistrationAPIView.as_view(), name='register')
]