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
