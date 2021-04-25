from rest_framework import authentication
from rest_framework import exceptions
from .models import CustomUser

class CoreBackendAuthentication(authentication.BaseAuthentication):
    def authenticate(email, password):
        print("athenticating")
        try:
            user = CustomUser.objects.get(email=email, password=password)
        except CustomUser.DoesNotExist:
            return None
        return user
