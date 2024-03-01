from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.parsers import MultiPartParser
from rest_framework import generics

from schedule_core.swagger_service.apply_swagger_auto_schema import apply_swagger_auto_schema
from users.serializers.forgot_password_serializer import ForgotPasswordSerializer
from users.permissions.is_blocked import IsBlocked


class ForgotPasswordView(generics.GenericAPIView):
    """
    View for resetting user password.

    When making a POST request to this view,
    the user password will be reset and a new password will be sent to the user's email.
    """
    permission_classes = [AllowAny, IsBlocked]
    serializer_class = ForgotPasswordSerializer
    parser_classes = [MultiPartParser]

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

        # create method of serializer is invoked to reset password and send email
        serializer.save()

        return Response(
            "Your new password has been sent successfully!",
            status=status.HTTP_200_OK
        )


ForgotPasswordView = apply_swagger_auto_schema(
    tags=['change / forgot password'], excluded_methods=[]
)(ForgotPasswordView)