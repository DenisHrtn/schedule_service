from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework.parsers import MultiPartParser

from users.models.user import User
from users.serializers.unblock_users_serializer import UnblockUsersSerializer
from users.permissions.is_superuser import IsSuperuser
from schedule_core.swagger_service.apply_swagger_auto_schema import apply_swagger_auto_schema
from users.services.email_service import EmailService


class UnblockUsersView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated, IsSuperuser]
    serializer_class = UnblockUsersSerializer
    parser_classes = [MultiPartParser]
    sender_service = EmailService()

    def put(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_email = serializer.validated_data['user_email']
        cause = serializer.validated_data['cause']

        try:
            user = User.objects.get(email=user_email)
            if user.is_superuser:
                return Response(
                    {'message': "User is super admin too"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            else:
                if user.is_active:
                    if user.is_blocked:
                        user.is_blocked = False
                        user.save()
                        self.sender_service.send_mail_after_unblocking(
                            email=user_email,
                            cause=cause
                        )
                    else:
                        return Response(
                            {'message': "User is not blocked"},
                            status=status.HTTP_400_BAD_REQUEST
                        )
                else:
                    return Response(
                        {'message': "User is not activated"},
                        status=status.HTTP_400_BAD_REQUEST
                    )
        except Exception as e:
            return Response(f"Something went wrong: {e}")

        return Response(
            {'message': "User has been unblocked"},
            status=status.HTTP_200_OK
        )


UnblockUsersView = apply_swagger_auto_schema(
    tags=['block / unblock'], excluded_methods=[]
)(UnblockUsersView)