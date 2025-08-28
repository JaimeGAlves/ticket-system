import os, json
import firebase_admin
from firebase_admin import credentials, auth as fb_auth
from rest_framework.authentication import BaseAuthentication, get_authorization_header
from rest_framework import exceptions
from django.utils import timezone
from .models import User

# init Firebase (uma vez)
_app = None
def init_firebase():
    global _app
    if _app:
        return _app
    raw = os.getenv("FIREBASE_CREDENTIALS_JSON")
    if not raw:
        raise RuntimeError("FIREBASE_CREDENTIALS_JSON ausente")
    cred = credentials.Certificate(json.loads(raw))
    _app = firebase_admin.initialize_app(cred)
    return _app

init_firebase()

class FirebaseAuthentication(BaseAuthentication):
    keyword = b"Bearer"

    def authenticate(self, request):
        auth = get_authorization_header(request).split()
        if not auth or auth[0].lower() != self.keyword.lower():
            return None
        if len(auth) != 2:
            raise exceptions.AuthenticationFailed("Authorization inválido")
        token = auth[1].decode("utf-8")
        try:
            decoded = fb_auth.verify_id_token(token)
        except Exception:
            raise exceptions.AuthenticationFailed("Token Firebase inválido/expirado")

        uid = decoded.get("uid")
        email = decoded.get("email")
        name = decoded.get("name") or (email.split("@")[0] if email else uid)

        user, _ = User.objects.update_or_create(
            firebase_uid=uid,
            defaults={
                "email": email or f"{uid}@noemail.local",
                "username": name,
                "last_login": timezone.now(),
            },
        )
        return (user, None)
