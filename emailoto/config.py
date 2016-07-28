from django.conf import settings


class EmailOtoConfig(object):

    def __init__(self):
        self.redis_host = settings.EMAILOTO_CONFIG.get('redis_host', default='localhost')
        self.redis_port = settings.EMAILOTO_CONFIG.get('redis_port', default=6379)
        self.redis_db = settings.EMAILOTO_CONFIG.get('redis_host', default=2)
        self.expiration = settings.EMAILOTO_CONFIG.get('expiration', default=60 * 10)
        self.template = settings.EMAILOTO_CONFIG.get('template', default='emailoto/default_template.html')
        self.mailgun_api_key = self.get_mailgun_api_key()
        self.mailgun_api_url = self.get_mailgun_api_url()
        self.sender = self.get_sender()

    class ImproperlyConfigured(Exception):
        pass

    def _raise(self, msg):
        """Raise a configutation message with a useful error."""
        raise self.ImproperlyConfigured(
            msg,
            '\nExample of a valid configuration in your settings.py file: \n'
            "\n\t EMAILOTO_CONFIG = {"
            "\n\t\t redis_host': 'localhost',"
            "\n\t\t'redis_port': 6379,"
            "\n\t\t'redis_db': 2,"
            "\n\t\t'expiration': 1,"
            "\n\t\t'mailgun_api_key': 'your-mailgun-key',"
            "\n\t\t'mailgun_api_url': 'your-mailgun-api-url',"
            "\n\t\t'sender': 'Your Name <yourname@yourdomain.com>',"
            "\n\t\t'template': 'yourapp/template_name.html'"
            "\n\t}"
        )

    @property
    def get_mailgun_api_key(self):
        value = settings.EMAILOTO_CONFIG.get('mailgun_api_key')
        if not value:
            self._raise('No "mailgun_api_key" found.')
        return value

    @property
    def get_mailgun_api_url(self):
        value = settings.EMAILOTO_CONFIG.get('mailgun_api_url')
        if not value:
            self._raise('No "mailgun_api_url" found.')
        return value

    @property
    def get_sender(self):
        """The sender shown for the authentication email."""
        value = settings.EMAILOTO_CONFIG.get('sender')
        if not value:
            self._raise('No "sender" found.')
        return value


CONFIG = EmailOtoConfig()
