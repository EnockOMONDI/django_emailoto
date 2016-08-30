from django.template import Context
from django.template.loader import get_template
from .authentication import EmailOtoAuthBackend
from django.utils.safestring import mark_safe
from .config import CONFIG
import requests
from ratelimit.decorators import ratelimit


def _create_template(request, email, template, success_url):
    template = get_template(template)
    url = EmailOtoAuthBackend.get_auth_url(email, success_url)
    context = Context({
        'auth_url': mark_safe(request.build_absolute_uri(url))
    })
    return template.render(context)


@ratelimit(key='ip', rate=CONFIG.ratelimit)
def send_email(request, to_email, sender, subject, template, success_url):
    return requests.post(
        "%s/messages" % CONFIG.mailgun_api_url,
        auth=("api", CONFIG.mailgun_api_key),
        data={
            "from": sender,
            "to": to_email,
            "subject": subject,
            "text": _create_template(request, to_email, template, success_url)
        }
    )
