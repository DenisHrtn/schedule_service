from django.db import models

from .schedule import Schedule


class Attachment(models.Model):
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    file = models.FileField(upload_to='attachments/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file.name
