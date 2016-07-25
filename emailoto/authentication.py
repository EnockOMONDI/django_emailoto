from django.contrib.auth.models import User
from emailoto.token_client import TokenClient


class EmailOtoAuthBackend(object):
    def authenticate(self, email_token, counter_token):
        """Authenticate a user given a email_ and counter_ token pair."""
        try:
            email = TokenClient().validate_token_pair(
                email_token, counter_token)
        except TokenClient.InvalidTokenPair:
            return False
        else:
            user, created = User.objects.get_or_create(username=email)
            return user
        return None

    def get_user(self, email):
        """Get the user associated with the given email address."""
        try:
            return User.objects.get(username=email)
        except User.DoesNotExist:
            return None
