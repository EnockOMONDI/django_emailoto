import redis
from django.conf import settings
import uuid
from emailoto.config import CONFIG


class TokenClient(object):

    def __init__(self):
        self._redis = redis.StrictRedis(
            host=CONFIG.redis_host,
            port=CONFIG.redis_port,
            db=CONFIG.redis_db
        )

    class InvalidTokenPair(Exception):
        pass

    def get_token_pair(self, email):
        """Return a counter/email token pair for the given email."""
        email_token = self._set_email(email)
        counter_token = self._set_counter()
        return email_token, counter_token

    def validate_token_pair(self, email_token, counter_token):
        """Validate the token pair; return the email if valid."""
        email = self._validate_email(email_token)
        if email and self._validate_counter(counter_token):
            return email
        raise self.InvalidTokenPair

    def _set_email(self, email):
        """Create a unique token key for the given email address."""
        token = uuid.uuid4().hex
        self._set_and_expire(token, email)
        return token

    def _validate_email(self, email_token):
        """Return the email address if the email token is valid."""
        return self._redis.get(email_token)

    def _set_counter(self):
        """Create a unique token with a counter and set it in Redis."""
        token = uuid.uuid4().hex
        self._set_and_expire(token, '0')
        return token

    def _set_and_expire(self, key, value):
        """Set the key-value pair to redis. Also set an expiration time."""
        self._redis.set(key, value)
        self._redis.expire(key, CONFIG.expiration)

    def _validate_counter(self, token):
        """Validate the given token. If it exists, increment its count.

        A token is invalid if it doesn't exist in redis, or if it has already
        been validated (the count > 0).
        """
        count = self._redis.get(token)
        if count and count.isdigit() and int(count) == 0:
            self._redis.incr(token)
            return True
        return False
