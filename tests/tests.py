from django.test import override_settings
from emailoto.token_client import TokenClient
from emailoto.authentication import EmailOtoAuthBackend
import time
from django.test.client import RequestFactory
from .test_base import EmailOtoTest
from emailoto import views
from django.core.urlresolvers import reverse


class TokenClientTest(EmailOtoTest):

    def test_set_counter(self):
        """Setting a token should put it in redis with a count of '0'."""
        tc = TokenClient()
        token = tc._set_counter()
        self.assertEqual(tc._redis.get(token), '0')

    def test_validate_counter(self):
        """A valid token with return True and increment the counter."""
        tc = TokenClient()
        token = tc._set_counter()
        self.assertTrue(tc._validate_counter(token))
        self.assertEqual(tc._redis.get(token), '1')

    def test_more_than_one_validation(self):
        """Only the first validation should return True."""
        tc = TokenClient()
        token = tc._set_counter()
        self.assertTrue(tc._validate_counter(token))
        self.assertFalse(tc._validate_counter(token))

    def test_invalid_token(self):
        """Non-existant keys should be False."""
        tc = TokenClient()
        self.assertFalse(tc._validate_counter('world'))

    def test_set_email(self):
        """Test setting an email and getting a token for that email."""
        tc = TokenClient()
        token = tc._set_email('test@example.com')
        self.assertEqual(tc._redis.get(token), 'test@example.com')

    def test_set_and_validate_email(self):
        """Set and validate an email."""
        tc = TokenClient()
        token = tc._set_email('test@example.com')
        self.assertEqual(tc._validate_email(token), 'test@example.com')

    def test_get_token_pair(self):
        e_token, c_token = TokenClient().get_token_pair('A@B.com')
        self.assertIsNotNone(e_token)
        self.assertIsNotNone(c_token)

    def test_validate_token_pair(self):
        e_token, c_token = TokenClient().get_token_pair('A@B.com')
        email_result = TokenClient().validate_token_pair(e_token, c_token)
        self.assertEqual(email_result, 'A@B.com')

    def test_multiple_validation_attempts(self):
        e_token, c_token = TokenClient().get_token_pair('A@B.com')
        TokenClient().validate_token_pair(e_token, c_token)
        with self.assertRaises(TokenClient.InvalidTokenPair):
            TokenClient().validate_token_pair(e_token, c_token)

    @override_settings(EMAILOTO_REDIS_KEY_EXPIRATION=1)
    def test_expired_email(self):
        """An email token should expire."""
        tc = TokenClient()
        token = tc._set_email('test@example.com')
        time.sleep(1.1)
        self.assertIsNone(tc._validate_email(token))

    @override_settings(EMAILOTO_REDIS_KEY_EXPIRATION=1)
    def test_expired_counter_token(self):
        """A counter token should expire."""
        tc = TokenClient()
        token = tc._set_counter()
        time.sleep(1.1)
        self.assertFalse(tc._validate_counter(token))

    @override_settings(EMAILOTO_REDIS_KEY_EXPIRATION=1)
    def test_expired_tokens(self):
        """Test both tokens at once for expiration."""
        e_token, c_token = TokenClient().get_token_pair('A@B.com')
        time.sleep(1.1)
        with self.assertRaises(TokenClient.InvalidTokenPair):
            TokenClient().validate_token_pair(e_token, c_token)


class AuthenticationTest(EmailOtoTest):

    def test_valid_auth(self):
        e_token, c_token = TokenClient().get_token_pair('A@B.com')
        backend = EmailOtoAuthBackend()
        user = backend.authenticate(e_token, c_token)
        self.assertEqual(user.username, 'A@B.com')

    def test_invalid_auth(self):
        backend = EmailOtoAuthBackend()
        user = backend.authenticate('fake-email-token', 'fake-counter-token')
        self.assertFalse(user)

    def test_valid_email_invalid_counter(self):
        e_token, c_token = TokenClient().get_token_pair('A@B.com')
        backend = EmailOtoAuthBackend()
        user = backend.authenticate(e_token, 'fake-counter-token')
        self.assertFalse(user)

    def test_invalid_email_valid_counter(self):
        e_token, c_token = TokenClient().get_token_pair('A@B.com')
        backend = EmailOtoAuthBackend()
        user = backend.authenticate('fake-email-token', c_token)
        self.assertFalse(user)


class ValidateViewsTest(EmailOtoTest):

    def test_valid_get_request(self):
        e_token, c_token = TokenClient().get_token_pair('A@B.com')
        factory = RequestFactory()
        url = reverse('emailoto-validate') + '?a=%s&b=%s' % (e_token, c_token)
        request = factory.get(url)
        response = views.validate(request)
        self.assertEqual(response.status_code, 200)

    def test_invalid_get_request(self):
        e_token, c_token = 'fake-email-token', 'fake-counter-token'
        factory = RequestFactory()
        url = reverse('emailoto-validate') + '?a=%s&b=%s' % (e_token, c_token)
        request = factory.get(url)
        response = views.validate(request)
        self.assertEqual(response.status_code, 403)
