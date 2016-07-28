from django.template import Context
from django.template.loader import get_template
from emailoto.authentication import EmailOtoAuthBackend
from django.utils.safestring import mark_safe
from emailoto.config import EmailOtoConfig
import requests


class EmailClient(object):

    def _create_template(self, request, email):
        template = get_template(EmailOtoConfig.template)
        url = EmailOtoAuthBackend.get_auth_url(email)
        context = Context({
            'auth_url': mark_safe(request.build_absolute_uri(url))
        })
        return template.render(context)

    def send_simple_message(self, request, email):
        return requests.post(
            "%s/messages" % EmailOtoConfig.mailgun_api_key,
            auth=("api", EmailOtoConfig.mailgun_api_url),
            data={
                "from": EmailOtoConfig.sender,
                "to": email,
                "subject": EmailOtoConfig.subject,
                "text": self._create_template(request, email)
            }
        )
