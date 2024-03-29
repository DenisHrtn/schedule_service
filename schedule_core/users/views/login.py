from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from rest_framework.parsers import MultiPartParser

from users.serializers.login_serializer import LoginSerializer
from schedule_core.swagger_service.apply_swagger_auto_schema import apply_swagger_auto_schema


class LoginView(generics.GenericAPIView):
    """
    View for user login.

    When making a POST request to this view,
    the user will be logged in and access and refresh tokens will be generated for the user.

    Parameters:
        - permission_classes ([AllowAny]):
            Permission classes for accessing this view.
            In this case, it allows any unauthenticated user.

        - serializer_class (LoginSerializer):
            Serializer for input data.
            It should validate and provide the required user information.

    Methods:
        - post(request):
            Handles POST requests for user login.
            If successful, access and refresh tokens will be generated and stored in cookies.

    """

    permission_classes = [AllowAny,]
    serializer_class = LoginSerializer
    parser_classes = [MultiPartParser, ]

    def post(self, request):
        """
        Handles POST request for user login.

        If the provided user data is valid,
        access and refresh tokens will be generated and stored in cookies.

        Response codes:
        - 200 (OK): User logged in successfully.
        - 400 (Bad Request): User validation error.
        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']

        if not user.is_active:
            return Response(
                'Your account is not active. Please try again.',
                status=status.HTTP_400_BAD_REQUEST
            )

        if user:
            access_token = AccessToken.for_user(user)
            refresh_token = RefreshToken.for_user(user)
            response = Response(
                {'message': 'Logged in successfully'}
            )
            response.set_cookie(key='access_token', value=access_token, httponly=True)
            response.set_cookie(key='refresh_token', value=refresh_token, httponly=True)
            return response
        else:
            response = Response(
                {'message': 'User validation error'}
            )
            return response


LoginView = apply_swagger_auto_schema(
    tags=['authentication / register'], excluded_methods=[]
)(LoginView)