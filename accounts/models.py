from django.db import models
from core.models import BaseModel

class User(BaseModel):
    username = models.CharField(max_length=150)
    password = models.CharField(max_length=255, blank=True)
    email = models.EmailField(unique=True)
    last_login = models.DateTimeField(null=True, blank=True)
    firebase_uid = models.CharField(max_length=128, unique=True, db_index=True)

    class Meta:
        indexes = [
            models.Index(fields=["email"]),
            models.Index(fields=["firebase_uid"]),
        ]

    def __str__(self):
        return self.username or self.email
