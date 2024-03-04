from django.db import models


class Denis(models.Model):
     age = models.IntegerField(blank=True)
     gender = models.CharField(max_length=15)

     class Meta:
          verbose_name = "денис"
          verbose_name_plural = 'дкенииисс'

     def __str__(self):
          return f'self.age'