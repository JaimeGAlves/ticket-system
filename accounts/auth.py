# accounts/auth.py
import os, json
from django.conf import settings
from rest_framework.authentication import BaseAuthentication, get_authorization_header
from rest_framework import exceptions
from django.contrib.auth import get_user_model

import firebase_admin
from firebase_admin import credentials, auth as fb_auth

User = get_user_model()

def _init_firebase():
    if firebase_admin._apps:
        return
    path = getattr(settings, "FIREBASE_CREDENTIALS_PATH", None)
    env_value = os.getenv("FIREBASE_CREDENTIALS_JSON") or os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

    if path and os.path.exists(path):
        cred = credentials.Certificate(str(path))
    elif env_value and os.path.exists(env_value):
        cred = credentials.Certificate(env_value)
    elif env_value:
        cred = credentials.Certificate(json.loads(env_value))
    else:
        raise RuntimeError("Credenciais do Firebase não configuradas")

    firebase_admin.initialize_app(cred)

class FirebaseAuthentication(BaseAuthentication):
    """
    Espera: Authorization: Bearer <ID_TOKEN_DO_FIREBASE>
    """
    def authenticate(self, request):
        _init_firebase()

        auth = get_authorization_header(request).split()

        if not auth or auth[0].lower() != b"bearer":
            return None

        if len(auth) == 1:
            raise exceptions.AuthenticationFailed("Authorization Bearer sem token")
        if len(auth) > 2:
            raise exceptions.AuthenticationFailed("Authorization Bearer malformado")

        token = auth[1].decode("utf-8")

        try:
            decoded = fb_auth.verify_id_token(token, check_revoked=True)
        except Exception as e:
            name = e.__class__.__name__
            if name == "ExpiredIdTokenError":
                msg = "Token expirado"
            elif name == "RevokedIdTokenError":
                msg = "Token revogado"
            elif name == "InvalidIdTokenError":
                msg = "Token inválido"
            else:
                msg = f"Falha ao validar token: {e}"
            raise exceptions.AuthenticationFailed(msg) from e

        uid = decoded.get("uid")
        email = decoded.get("email") or f"{uid}@firebase.local"

        user, _ = User.objects.get_or_create(username=uid, defaults={"email": email})
        return (user, None)
