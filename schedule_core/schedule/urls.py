from django.urls import path, include
from rest_framework.routers import DefaultRouter

from schedule.views import ScheduleViewSet

router = DefaultRouter()
router.register('schedule', ScheduleViewSet, basename='schedule')

urlpatterns = [

] + router.urls
