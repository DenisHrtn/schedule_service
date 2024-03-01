from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model
from rest_framework import generics
from rest_framework.parsers import MultiPartParser

from users.serializers.register_serializer import RegisterSerializer
from schedule_core.swagger_service.apply_swagger_auto_schema import apply_swagger_auto_schema


User = get_user_model()


class RegistrationAPIView(generics.GenericAPIView):
    """
    View for user registration.

    When making a POST request to this view,
    the user will be registered and a verification code will be sent to their email.

    Parameters:
        - permission_classes ([AllowAny]):
            Permission classes for accessing this view.
            In this case, it allows any unauthenticated user.

        - serializer_class (RegisterSerializer):
            Serializer for input data.
            It should validate and provide the required user information.

    Methods:
        - post(request):
            Handles POST requests for user registration.
            If successful, a verification code will be sent to the user's email.
    """
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer
    parser_classes = [MultiPartParser, ]

    def post(self, request):
        """
        Handles POST request for user registration.

        If the provided user data is valid,
        the user will be registered and a verification code will be sent to their email.

        Response codes:
            - 201 (Created): User registered successfully and code has been sent.
            - 400 (Bad Request): User validation error or missing fields.
        """

        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Code has been sent"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


RegistrationAPIView = apply_swagger_auto_schema(
    tags=['authentication / register'], excluded_methods=[]
)(RegistrationAPIView)