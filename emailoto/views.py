from django.views.decorators.http import require_GET
from django.http import HttpResponse, HttpResponseForbidden
from emailoto.token_client import TokenClient
from ratelimit.decorators import ratelimit
from emailoto.config import CONFIG


@require_GET
@ratelimit(key='ip', rate=CONFIG.ratelimit)
def validate(request):
    """Validate an authentication request."""
    email_token = request.GET.get('a')
    client_token = request.GET.get('b')
    try:
        TokenClient().validate_token_pair(email_token, client_token)
        return HttpResponse()
    except TokenClient.InvalidTokenPair:
        return HttpResponseForbidden()
