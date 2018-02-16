"""
Definition of models.
"""

from django.db import models
from django.utils import timezone

# Model for API keys

class apiKey(models.Model):
    api_key = models.CharField(max_length=64)
    date_creation = models.DateTimeField(default=timezone.now)
    date_expiration = models.DateTimeField(default=timezone.now)


    def __str__(self):
         return self.api_key