"""
Definition of models.
"""

import logging
import pymongo

from django.db import models
from django.utils import timezone
from django.core.validators import RegexValidator

validate_even = RegexValidator(r"^\w{4}([-]?\w{4}){3}", "La clé doit être de la forme 0000-0000-0000-0000 avec des caractères alphanumériques.")

# Model for API keys

class MongoHandler():
    def __init__(self, host: str='localhost', port: int=27017, **kwargs) -> None:
        self.logger = logging.getLogger()
        self.client = pymongo.MongoClient(
            host,
            port,
            connect=True,
            serverSelectionTimeoutMS=3000,
            connectTimeoutMS=3000,
            socketTimeoutMS=3000)
        self.set_db(kwargs.get('db', None))
        self.set_collection(kwargs.get('collection', None))

    def set_db(self, db: str):
        if db:
            self.db = self.client[db]
        else:
            self.db = None

    def set_collection(self, collection: str):
        if self.db and collection:
            self.collection = self.db[collection]
        else:
            self.db = None

    def ping(self) -> bool:
        try:
            self.db.command('ping')
        except pymongo.errors.ServerSelectionTimeoutError:
            return False
        return True


class apiKey(models.Model):
    api_key = models.CharField(max_length=19, validators=[validate_even])
    date_creation = models.DateTimeField(default=timezone.now)
    date_expiration = models.DateTimeField(default=timezone.now)

    def __str__(self):
         return self.api_key
