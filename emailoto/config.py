from django.conf import settings


class EmailOtoConfig(object):

    def __init__(self):
        """Read from settings.py and apply defaults (or raise exceptions.)"""

        self.redis_host = settings.EMAILOTO.get('redis_host', 'localhost')
        self.redis_port = settings.EMAILOTO.get('redis_port', 6379)
        self.redis_db = settings.EMAILOTO.get('redis_db', 2)
        self.expiration = settings.EMAILOTO.get('expiration', 60 * 10)
        self.template = settings.EMAILOTO.get('template', 'emailoto/default_template.html')  # NOQA
        self.ratelimit = settings.EMAILOTO.get('ratelimit', '5/m')

        self.mailgun_api_key = self.get_or_raise('mailgun_api_key')
        self.mailgun_api_url = self.get_or_raise('mailgun_api_url')
        self.sender = self.get_or_raise('sender')

    class ImproperlyConfigured(Exception):
        pass

    def get_or_raise(self, setting_key):
        value = settings.EMAILOTO.get(setting_key)
        if not value:
            raise self.ImproperlyConfigured(
                'No "%s" found in settings.py configuration.' % (setting_key)
            )
        return value


CONFIG = EmailOtoConfig()
