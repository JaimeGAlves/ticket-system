from django.db import transaction
from django.core.exceptions import ValidationError
from .models import Event, EventGuest

@transaction.atomic
def subscribe_user(event: Event, user):
    event = Event.objects.select_for_update().get(pk=event.pk)
    if not event.is_active: raise ValidationError("Evento inativo")
    if event.guests.count() >= event.max_subscription:
        raise ValidationError("Limite de vagas atingido")
    conflict = EventGuest.objects.filter(
        user=user,
        event__starts_at__lt=event.ends_at,
        event__ends_at__gt=event.starts_at,
    ).exists()
    if conflict: raise ValidationError("Conflito de horário com outro evento")
    EventGuest.objects.get_or_create(event=event, user=user)

@transaction.atomic
def unsubscribe_user(event: Event, user):
    EventGuest.objects.filter(event=event, user=user).delete()