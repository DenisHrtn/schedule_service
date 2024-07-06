from django.db import models

from .mark import Mark
from .category import Category
from users.models import User


class Schedule(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=False, null=False)
    due_date = models.DateField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='schedules_categories')
    mark = models.ForeignKey(Mark, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='schedules_users')
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
