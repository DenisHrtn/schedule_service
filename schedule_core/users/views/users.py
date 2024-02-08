from rest_framework import generics
from rest_framework.response import Response
from rest_framework import permissions, status
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser

from users.models.user import User
from users.serializers.users_serializer import UserSerializer
from schedule_core.swagger_service.apply_swagger_auto_schema import apply_swagger_auto_schema
from users.permissions.is_blocked import IsBlocked


class UsersAPIView(generics.GenericAPIView):
    """
    API view for retrieving all active and unblocked users.
    """
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, IsBlocked]
    parser_classes = [MultiPartParser, ]

    @action(methods=['GET'], detail=False)
    def get(self, request):
        """
        Retrieve all active and unblocked users.

        Returns:
            - Response:
                - 200 (OK): Returns the list of users.
                - 403 (FORBIDDEN): Returns an error message if the user is not logged in.
        """
        if request.user.is_superuser:
            users = User.objects.exclude(is_superuser=True)
            return Response(UserSerializer(users, many=True).data, status=status.HTTP_200_OK)
        else:
            users = User.objects.filter(is_blocked=False, is_active=True).exclude(is_superuser=True)
            return Response(UserSerializer(users, many=True).data, status=status.HTTP_200_OK)


class UserDetailAPIView(generics.GenericAPIView):
    """
    API view for retrieving specific user details.
    """
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, IsBlocked]
    parser_classes = [MultiPartParser, ]

    @action(methods=['GET'], detail=True, url_path='users/(?P<user_id>\d+)')
    def get(self, request, *args, **kwargs):
        """
        Retrieve user details by their ID.

        Parameters:
            - user_id (int):
            The ID of the user.

        Returns:
            - Response:
                - 200 (OK): Returns the user details.
                - 403 (FORBIDDEN): Returns an error message if the user is blocked or not active.
              """
        user_id = kwargs.get('user_id')
        user = User.objects.filter(id=user_id).first()
        if user.is_blocked or not user.is_active:
            return Response(
                "This user is blocked or not activated",
                status=status.HTTP_403_FORBIDDEN
            )
        elif user.is_superuser:
            return Response(
                "This user is superuser",
                status=status.HTTP_403_FORBIDDEN
            )
        else:
            return Response(UserSerializer(user, many=False).data)


UsersAPIView = apply_swagger_auto_schema(
    tags=['users'], excluded_methods=[]
)(UsersAPIView)

UserDetailAPIView = apply_swagger_auto_schema(
    tags=['users'], excluded_methods=[]
)(UserDetailAPIView)