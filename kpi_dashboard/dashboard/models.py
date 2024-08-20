# dashboard/models.py
from django.db import models

class KPI(models.Model):
    key = models.CharField(max_length=255)
    value = models.FloatField()

    def __str__(self):
        return f"{self.key}: {self.value}"
