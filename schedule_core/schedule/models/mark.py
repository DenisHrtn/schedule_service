from django.db import models


class Mark(models.Model):
    HIGH = 'high'
    MEDIUM = 'medium'
    LOW = 'low'

    CHOICES = (
        (HIGH, 'высокий'),
        (MEDIUM, 'средний'),
        (LOW, 'низкий'),
    )

    value = models.CharField(max_length=20, choices=CHOICES)

    def __str__(self):
        return self.value
