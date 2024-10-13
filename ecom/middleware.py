# ecom/middleware.py

from django.shortcuts import redirect
from django.conf import settings
from django.contrib import messages


class CustomLoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated and 'login' not in request.path:
            messages.error(request, 'Devi effettuare il login per accedere a questa pagina.')
            return redirect(settings.LOGIN_URL)

        return self.get_response(request)