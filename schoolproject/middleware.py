from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth.models import AnonymousUser
from rest_framework import exceptions

class JWTAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            authenticated = JWTAuthentication().authenticate(request)
            if authenticated:
                request.user = authenticated[0]
            else:
                request.user = AnonymousUser
        except exceptions.AuthenticationFailed as err:
            print(err)
            request.user = AnonymousUser

        response = self.get_response(request)
        return response
