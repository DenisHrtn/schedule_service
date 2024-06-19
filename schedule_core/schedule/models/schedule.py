from django.db import models

from .mark import Mark
from .category import Category


class Schedule(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=False, null=False)
    due_date = models.DateField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    mark = models.ForeignKey(Mark, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
