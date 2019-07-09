import re

from django.conf import settings
from django.shortcuts import redirect


class RequireLoginMiddleware(object):

    def __init__(self, get_response):
         # One-time configuration and initialization.
        self.get_response = get_response

        self.required = tuple(re.compile(url)
                              for url in settings.LOGIN_REQUIRED_URLS)
        self.exceptions = tuple(re.compile(url)
                                for url in settings.LOGIN_REQUIRED_URLS_EXCEPTIONS)

    def __call__(self, request):

        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):

        # No need to process URLs if email already logged in
        try:
            email = request.session['email']
        except:
            email = None

        if email is not None:
            return None

        # An exception match should immediately return None
        for url in self.exceptions:
            if url.match(request.path):
                return None

        # Requests matching a restricted URL pattern are returned
        # wrapped with the login_required decorator
        for url in self.required:
            if email is None:
                if url.match(request.path):
                    return redirect('login')
            return None
        # Explicitly return None for all non-matching requests
        return redirect('login')
