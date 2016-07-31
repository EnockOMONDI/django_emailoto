from django.views.decorators.http import require_GET
from django.http import HttpResponseForbidden
from ratelimit.decorators import ratelimit
from .config import CONFIG
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect


@require_GET
@ratelimit(key='ip', rate=CONFIG.ratelimit)
def validate(request):
    """Validate an authentication request."""
    email_token = request.GET.get('a')
    client_token = request.GET.get('b')
    user = authenticate(email_token=email_token, counter_token=client_token)
    if user:
        login(request, user)
        return redirect(CONFIG.login_redirect)
    else:
        return HttpResponseForbidden()
