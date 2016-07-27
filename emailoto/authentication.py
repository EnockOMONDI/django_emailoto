from django.contrib.auth.models import User
from emailoto.token_client import TokenClient
from django.core.urlresolvers import reverse


class EmailOtoAuthBackend(object):

    @staticmethod
    def authenticate(email_token, counter_token):
        """Authenticate a user given a email_ and counter_ token pair."""
        try:
            email = TokenClient().validate_token_pair(
                email_token, counter_token)
        except TokenClient.InvalidTokenPair:
            return False
        else:
            user, _ = User.objects.get_or_create(username=email)
            return user
        return None

    @staticmethod
    def get_user(email):
        """Get the user associated with the given email address."""
        try:
            return User.objects.get(username=email)
        except User.DoesNotExist:
            return None

    @staticmethod
    def get_auth_url(email):
        """Construct the auth_url for  a given email."""
        email_token, client_token = TokenClient().get_token_pair(email)
        url = reverse('emailoto-validate')
        return url + '?a=%s&b=%s' % (email_token, client_token)
