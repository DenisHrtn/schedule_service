from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser
from django.contrib.auth.hashers import check_password

from users.serializers.change_password_serializer import ChangePasswordSerializer
from schedule_core.swagger_service.apply_swagger_auto_schema import apply_swagger_auto_schema
from users.permissions.is_blocked import IsBlocked


class ChangePasswordView(generics.GenericAPIView):
    """
    View for changing user password.

    When making a POST request to this view,
    the user password will be changed to a new password.

    Parameters:
        - permission_classes ([IsAuthenticated, IsBlocked]):
            Permission classes for accessing this view.
            In this case, it requires the user to be authenticated and not blocked.

        - serializer_class (ChangePasswordSerializer):
            Serializer for input data.
            It should validate and provide the required user information.

    Methods:
        - post(request):
            Handles POST requests for changing user password.
            If successful, the user password will be changed to a new password.

    """
    permission_classes = [IsAuthenticated, IsBlocked]
    serializer_class = ChangePasswordSerializer
    parser_classes = [MultiPartParser]

    def post(self, request):
        """
        Handles POST request for changing user password.

        If the provided user data is valid and the old password matches,
        the user password will be changed to a new password.

        Response codes:
        - 200 (OK): Password changed successfully.
        - 400 (Bad Request): Incorrect old password.
        """

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = request.user

        old_password = serializer.validated_data.get('old_password')
        new_password = serializer.validated_data.get('new_password')

        if not check_password(old_password, user.password):
            return Response(
                "Your old password does not match. If you forgot it, go to recovery.",
                status=status.HTTP_400_BAD_REQUEST
            )
        user.set_password(new_password)
        user.save()

        return Response(
            "Your password has been updated.",
            status=status.HTTP_200_OK
        )


ChangePasswordView = apply_swagger_auto_schema(
    tags=['change / forgot password'], excluded_methods=[]
)(ChangePasswordView)