from django.db import models
from core.models import BaseModel
from accounts.models import User

class Event(BaseModel):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owned_events")
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    address = models.CharField(max_length=255)
    complement = models.CharField(max_length=255, blank=True)
    zipcode = models.CharField(max_length=10)
    number = models.CharField(max_length=20, blank=True)
    city = models.CharField(max_length=120)
    state = models.CharField(max_length=2)
    starts_at = models.DateTimeField()
    ends_at = models.DateTimeField()
    max_subscription = models.PositiveIntegerField(default=1)
    is_active = models.BooleanField(default=True)

    class Meta:
        indexes = [
            models.Index(fields=["is_active", "starts_at"]),
            models.Index(fields=["zipcode"]),
            models.Index(fields=["state", "city"]),
        ]

class EventGuest(BaseModel):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="guests")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="subscriptions")

    class Meta:
        constraints = [models.UniqueConstraint(fields=["event","user"], name="uniq_event_user")]
        indexes = [models.Index(fields=["event"]), models.Index(fields=["user"])]
