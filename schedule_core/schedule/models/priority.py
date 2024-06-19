from django.db import models


class Priority(models.Model):
    name = models.CharField(max_length=255)
    level = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return self.name
