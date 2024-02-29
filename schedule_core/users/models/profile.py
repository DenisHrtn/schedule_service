from django.db import models
from django.utils import timezone

from .user import User


class SexChoices(models.TextChoices):
    MALE = "M", "Male"
    FEMALE = "F", "Female"


class TargetChoices(models.TextChoices):
    WORK = "WORK", "Just for work"
    DISCIPLINE = "DISCIPLINE", "For upgrade discipline"
    TIME_MANAGEMENT = "TIME_MANAGEMENT", "For time-management"
    OTHER = "OTHER", "Other options"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    first_name = models.CharField(max_length=25, blank=True, default='New')
    last_name = models.CharField(max_length=25, blank=True, default='User')
    about_me = models.TextField(blank=True, default='About')
    sex = models.CharField(
        max_length=64,
        choices=SexChoices.choices,
        default='',
        help_text="Пол",
        blank=True,
        null=True,
    )
    photo = models.ImageField(
        upload_to='avatars/',
        default='',
        null=True,
        blank=True,
    )
    city = models.CharField(max_length=45, blank=True, default='')
    country = models.CharField(max_length=45, blank=True, default='')
    use_service_for = models.CharField(
        max_length=64,
        choices=TargetChoices.choices,
        default='',
        blank=True,
        null=True,
        help_text="Цель использования сервиса"
    )
    days_with_service = models.DateTimeField(default=timezone.now,)