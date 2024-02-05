from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.parsers import MultiPartParser
from rest_framework import generics

from users.models.user import User
from users.serializers.confirmation_register_serializer import ConfirmationRegisterSerializer
from schedule_core.swagger_service.apply_swagger_auto_schema import apply_swagger_auto_schema


class ConfirmationRegisterView(generics.GenericAPIView):
    """
    View for confirming user registration.

    When making a POST request to this view,
    the user registration will be confirmed and the user will be activated.

    Parameters:
        - permission_classes ([AllowAny]):
            Permission classes for accessing this view.
            In this case, it allows any unauthenticated user.

        - serializer_class (ConfirmationRegisterSerializer):
            Serializer for input data.
            It should validate and provide the required user information.

    Methods:
        - post(request):
            Handles POST requests for confirming user registration.
            If successful, the user will be activated and the registration code will be verified.

    """
    serializer_class = ConfirmationRegisterSerializer
    permission_classes = [AllowAny, ]
    parser_classes = [MultiPartParser, ]

    def post(self, request):
        """
        Handles POST request for confirming user registration.

        If the provided user data is valid and the registration code is correct,
        the user will be activated and the registration will be confirmed.

        Response codes:
        - 200 (OK): Registration confirmed successfully.
        - 400 (Bad Request): Registration validation error.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        code_ = serializer.validated_data['code']

        try:
            user = User.objects.get(email=email, is_active=False)
            if user.validate_confirmation_code(code=user.code):
                if user.code == code_:
                    user.is_active = True
                    user.code = None
                    user.save()
                    return Response(
                        "The code was successfully verified.",
                        status=status.HTTP_200_OK
                    )
                else:
                    return Response(
                        "Incorrect code",
                        status=status.HTTP_400_BAD_REQUEST
                    )
            else:
                user.delete()
                return Response(
                    "The verification code has expired. Please register again.",
                    status=status.HTTP_400_BAD_REQUEST
                )
        except User.DoesNotExist:
            return Response(
                'User does not exist',
                status=status.HTTP_400_BAD_REQUEST
            )




ConfirmationRegisterView = apply_swagger_auto_schema(
    tags=['authentication / register'], excluded_methods=[]
)(ConfirmationRegisterView)