from django.db import models
from django.conf import settings

from .category import Category
from users.models import User


class Priority(models.TextChoices):
    HIGH = 'H', 'High'
    MEDIUM = 'M', 'Medium'
    LOW = 'L', 'Low'


class Schedule(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=False, null=False)
    due_date = models.DateField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='schedules_categories')
    mark = models.CharField(max_length=1, choices=Priority.choices, default=Priority.HIGH)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='schedules_history',
        default=settings.AUTH_USER_MODEL,
    )
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
