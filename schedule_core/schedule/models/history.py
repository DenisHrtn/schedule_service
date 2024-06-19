from django.db import models

from .schedule import Schedule


class History(models.Model):
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    changed_at = models.DateTimeField(auto_now=True)
    changes = models.TextField()

    def __str__(self):
        return f"{self.schedule.title} - {self.changed_at}"
