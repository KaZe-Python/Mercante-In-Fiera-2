from rest_framework import status
from rest_framework.exceptions import APIException

class NoAuthToken(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = "Authentication token is missing"
    default_code = "no_auth_token"

class InvalidAuthToken(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = "An invalid authentication token was provided"
    default_code = "invalid_token"

class FirebaseError(APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = "The provided auth token is not a valid Firebase User"
    default_code = "no_firebase_uid"