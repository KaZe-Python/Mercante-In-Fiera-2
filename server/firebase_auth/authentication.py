import os
import json

import firebase_admin
from firebase_admin import credentials
from firebase_admin import auth
from rest_framework import authentication

from django.contrib.auth.models import User
from django.utils import timezone


from .exceptions import FirebaseError
from .exceptions import NoAuthToken
from .exceptions import InvalidAuthToken

cred = credentials.Certificate("../../../private/mifv2-c0673-firebase-adminsdk-wduit-e891d86000.json")

default_app = firebase_admin.initialize_app(cred)

class FirebaseAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):

        auth_header = request.META.get("HTTP_AUTHORIZATION")
        if not auth_header:
            return NoAuthToken("No auth token was passed")
        
        id_token = auth_header.split(" ").pop()
        decoded_token = None

        try:
            decoded_token = auth.verify_id_token(id_token)
        except Exception:
            raise InvalidAuthToken("Invalid auth token")

        if not id_token or not decoded_token:
            return None

        try:
            uid = decoded_token.get("uid")
        except Exception:
            raise FirebaseError()
        
        user, created = User.objects.get_or_create(username=uid)
        user.profile.last_activity = timezone.localtime()

        return (user, None)