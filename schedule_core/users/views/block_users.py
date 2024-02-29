from rest_framework import status
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser

from users.models.user import User
from users.serializers.block_users_serializer import BlockUsersSerializer
from users.permissions.is_superuser import IsSuperuser
from users.services.email_service import EmailService
from schedule_core.swagger_service.apply_swagger_auto_schema import apply_swagger_auto_schema


class BlockUsersView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated, IsSuperuser]
    serializer_class = BlockUsersSerializer
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
                    {'message': "User is superuser too"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            else:
                if user.is_active:
                    if not user.is_blocked:
                        user.is_blocked = True
                        user.save()
                        self.sender_service.send_mail_before_blocking(
                            email=user_email,
                            cause=cause
                        )
                    else:
                        return Response(
                            {'message': "User already blocked"},
                            status=status.HTTP_400_BAD_REQUEST
                        )
                else:
                    return Response(
                        {'message': "User not activated"},
                        status=status.HTTP_400_BAD_REQUEST
                    )
        except Exception as e:
            return Response(f"Something went wrong: {e}", status=status.HTTP_400_BAD_REQUEST)
        return Response(
            {"message": "User blocked."},
            status=status.HTTP_200_OK
        )


BlockUsersView = apply_swagger_auto_schema(
    tags=['block / unblock'], excluded_methods=[]
)(BlockUsersView)