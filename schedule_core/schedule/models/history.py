from django.db import models
from django.contrib.postgres.fields import ArrayField

from .schedule import Schedule
from users.models import User


class History(models.Model):
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='user_history', on_delete=models.CASCADE)
    changed_at = models.DateTimeField(auto_now=True)
    changes = ArrayField(models.TextField())

    def __str__(self):
        return f"{self.schedule.title} - {self.changed_at}"
