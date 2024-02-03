from django.contrib.auth import logout
from django.http import HttpResponse
from rest_framework import permissions, serializers
from rest_framework import generics

from schedule_core.swagger_service.apply_swagger_auto_schema import apply_swagger_auto_schema


class EmptySerializer(serializers.Serializer):
    pass


class LogoutView(generics.GenericAPIView):
    """
    View for user logout.

    When making a POST request to this view,
    the user will be logged out and the access and refresh tokens
    stored in cookies will be deleted.

    Parameters:
        - serializer_class (EmptySerializer):
            Serializer for input data.
            In this case, EmptySerializer is used, which does not require any data validation.

        - permission_classes ([permissions.AllowAny]):
            Permission classes for accessing this view.
            In this case, it allows any unauthenticated user.

    Methods:
        - post(request):
            Handles POST requests.
            The user will be logged out and the tokens will be deleted from cookies.

    """
    serializer_class = EmptySerializer
    permission_classes = [permissions.AllowAny,]

    def post(self, request):
        """
        Handles POST request for user logout.

        The user will be logged out and the tokens will be deleted from cookies.

        Response codes:
        - 200 (OK): User logged out successfully.
        """
        logout(request)
        responce = HttpResponse(status=200)
        responce.delete_cookie('access_token')
        responce.delete_cookie('refresh_token')
        return responce


LogoutView = apply_swagger_auto_schema(
    tags=['authentication / register'], excluded_methods=[]
)(LogoutView)