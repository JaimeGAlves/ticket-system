import uuid
from django.db import models
from django.utils import timezone

class BaseModel(models.Model):
    id = models.BigAutoField(primary_key=True)
    uuid_code = models.UUIDField(default=uuid.uuid4, unique=True, db_index=True)
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True
        ordering = ("-created_at",)

class User(BaseModel):
    username = models.CharField(max_length=150)
    password = models.CharField(max_length=255, blank=True)  # não usada com Firebase
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
