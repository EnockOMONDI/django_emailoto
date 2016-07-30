from django.template import Context
from django.template.loader import get_template
from emailoto.authentication import EmailOtoAuthBackend
from django.utils.safestring import mark_safe
from emailoto.config import CONFIG
import requests
from ratelimit.decorators import ratelimit


def _create_template(request, email):
    template = get_template(CONFIG.template)
    url = EmailOtoAuthBackend.get_auth_url(email)
    context = Context({
        'auth_url': mark_safe(request.build_absolute_uri(url))
    })
    return template.render(context)


@ratelimit(key='ip', rate=CONFIG.ratelimit)
def send(request, email):
    return requests.post(
        "%s/messages" % CONFIG.mailgun_api_url,
        auth=("api", CONFIG.mailgun_api_key),
        data={
            "from": CONFIG.sender,
            "to": email,
            "subject": CONFIG.subject,
            "text": _create_template(request, email)
        }
    )
