from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.parsers import MultiPartParser
from rest_framework import generics

from users.models.user import User
from schedule_core.swagger_service.apply_swagger_auto_schema import apply_swagger_auto_schema
from users.serializers.forgot_password_serializer import ForgotPasswordSerializer
from users.services.email_service import EmailService
from users.permissions.is_blocked import IsBlocked


class ForgotPasswordView(generics.GenericAPIView):
    """
    View for resetting user password.

    When making a POST request to this view,
    the user password will be reset and a new password will be sent to the user's email.

    Parameters:
        - permission_classes ([AllowAny]):
            Permission classes for accessing this view.
            In this case, it allows any unauthenticated user.

        - serializer_class (ForgotPasswordSerializer):
            Serializer for input data.
            It should validate and provide the required user information.

    Methods:
        - post(request):
            Handles POST requests for resetting user password.
            If successful, the user password will be reset and a new password will be sent to the user's email.

    """
    permission_classes = [AllowAny, IsBlocked]
    serializer_class = ForgotPasswordSerializer
    parser_classes = [MultiPartParser]
    sender_service = EmailService()

    def post(self, request):
        """
        Handles POST request for resetting user password.

        If the provided user data is valid,
        the user password will be reset and a new password will be sent to the user's email.

        Response codes:
        - 200 (OK): Password reset and new password sent successfully.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        user = User.objects.get(email=email)

        new_password = User.objects.make_random_password(length=11)

        user.set_password(new_password)
        user.save()

        subject = "Your new password"
        message = ("Your new password has been updated!"
                   f"Your new password - {new_password}")
        self.sender_service.send_mail(
            email=email,
            subject=subject,
            message=message
        )

        return Response(
            "Your new password has been sent successfully!",
            status=status.HTTP_200_OK
        )


    # TODO Написать эндпоинт для смены инфы о юзере(включая профиль), пользователь должен иметь опцию запрета показа другим своего профиля

ForgotPasswordView = apply_swagger_auto_schema(
    tags=['change / forgot password'], excluded_methods=[]
)(ForgotPasswordView)