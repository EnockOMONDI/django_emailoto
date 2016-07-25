from django.test import TestCase
from emailoto.token_client import TokenClient


class EmailOtoTest(TestCase):
    def setUp(self):
        """Flush the test redis db before running tests."""
        TokenClient()._redis.flushdb()

    def tearDown(self):
        """Flush the test redis db after all tests."""
        TokenClient()._redis.flushdb()
