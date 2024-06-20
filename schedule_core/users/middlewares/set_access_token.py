from django.http import JsonResponse
from users.services.authentication import CustomAuthentication

custom_authentication_instance = CustomAuthentication()


class SetAccessTokenMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user, new_access_token = custom_authentication_instance.authenticate(request)

        if user and new_access_token:
            response = JsonResponse({'message': 'The new access_token'})
            response.set_cookie('access_token', str(new_access_token), httponly=True)
            request.access_token = str(new_access_token)
        else:
            response = self.get_response(request)

        return response
