from django.db import models

from .schedule import Schedule
from users.models.user import User


class Comment(models.Model):
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} - {self.schedule.title}"
