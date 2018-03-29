"""
Definition of models.
"""

from django.db import models
from django.utils import timezone
from django.core.validators import RegexValidator

validate_even = RegexValidator(r"^\w{4}([-]?\w{4}){3}", "La clé doit être de la forme 0000-0000-0000-0000 avec des caractères alphanumériques.")

# Model for API keys

class apiKey(models.Model):
    api_key = models.CharField(max_length=19, validators=[validate_even])
    date_creation = models.DateTimeField(default=timezone.now)
    date_expiration = models.DateTimeField(default=timezone.now)

    def __str__(self):
         return self.api_key
