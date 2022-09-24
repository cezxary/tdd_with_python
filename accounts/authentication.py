from accounts.models import Token, User
from django.contrib.auth.backends import BaseBackend


class PasswordlessAuthenticationBackend(BaseBackend):

    def authenticate(self, uid, **kwargs):
        try:
            token = Token.objects.get(uid=uid)
            return User.objects.get(email=token.email)
        except Token.DoesNotExist:
            return None
        except User.DoesNotExist:
            return User.objects.create(email=token.email)

    def get_user(self, email):
        try:
            return User.objects.get(email=email)
        except User.DoesNotExist:
            return None
