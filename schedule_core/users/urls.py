from django.urls import path
from rest_framework import routers

from users.views.registration import RegistrationAPIView

router = routers.DefaultRouter()

urlpatterns = [
    path('api/register/', RegistrationAPIView.as_view(), name='register')
]