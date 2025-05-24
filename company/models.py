from django.db import models
from core.models import TimeStampedModel

class Company(TimeStampedModel):
    name = models.CharField(max_length=100)
    tax_id = models.CharField(max_length=30, blank=True)
    address = models.TextField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name