from django.contrib.auth.models import User
from .token_client import TokenClient
from django.core.urlresolvers import reverse
import uuid
from django.db import transaction


class EmailOtoAuthBackend(object):

    @transaction.atomic
    def authenticate(self, email_token, counter_token):
        """Authenticate a user given a email_ and counter_ token pair."""
        try:
            email = TokenClient().validate_token_pair(
                email_token, counter_token)
        except TokenClient.InvalidTokenPair:
            return None
        else:
            user, _ = User.objects.get_or_create(
                email=email,
                defaults={'username': self._random_username()}
            )
            return user
        return None

    @staticmethod
    def get_user(user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

    @staticmethod
    def get_auth_url(email):
        """Construct the auth_url for  a given email."""
        email_token, client_token = TokenClient().get_token_pair(email)
        url = reverse('emailoto-validate')
        return url + '?a=%s&b=%s' % (email_token, client_token)

    @staticmethod
    def _random_username():
        """Generate a random username that is not already taken."""
        while True:
            username = uuid.uuid4().hex[:30]
            if not User.objects.filter(username=username).exists():
                return username
