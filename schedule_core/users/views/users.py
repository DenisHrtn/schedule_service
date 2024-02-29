from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import permissions, status
from drf_yasg.utils import swagger_auto_schema

from users.models.user import User
from users.serializers import UserSerializer, UserPatchSerializer
from users.permissions.is_blocked import IsBlocked


class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing users.

    When making requests to this ViewSet, it allows retrieving a list of users and partially updating user information.

    Parameters:
        - permission_classes ([permissions.IsAuthenticated, IsBlocked]):
            Permission classes for accessing this ViewSet.
            In this case, it allows only authenticated and not blocked users.

        - serializer_class (UserSerializer):
            Serializer for input data.
            It should validate and provide required user information.

    Methods:
        - get_queryset(*args, **kwargs):
            Returns a queryset to be used for retrieving the list of users.
            If the user is a superuser, it returns all users excluding the superuser themselves.
            If the user is authenticated, it returns only active and not blocked users excluding superusers.

        - create(request, *args, **kwargs):
            Handles POST requests for creating a new user.
            In this case, this method is not allowed.

        - destroy(request, *args, **kwargs):
            Handles DELETE requests for deleting a user.
            In this case, this method is not allowed.

        - update(request, *args, **kwargs):
            Handles PUT requests for updating user information.
            In this case, this method is not allowed.

        - partial_update(request, *args, **kwargs):
            Handles PATCH requests for partially updating user information.
            If the data is valid, user information is updated.
    """
    permission_classes = [permissions.IsAuthenticated, IsBlocked]
    serializer_class = UserSerializer

    def get_queryset(self, *args, **kwargs):
        """
        Returns a queryset to be used for retrieving the list of users.

        If the user is a superuser, it returns all users excluding the superuser themselves.
        If the user is authenticated, it returns only active and not blocked users excluding superusers.

        Response codes:
        - 200 (OK): The queryset is successfully returned.
        """
        if self.request.user.is_superuser:
            return User.objects.exclude(id=self.request.user.id)
        if self.request.user:
            return User.objects.filter(is_blocked=False, is_active=True).exclude(is_superuser=True)

    @swagger_auto_schema(auto_schema=None)
    def create(self, request, *args, **kwargs):
        """
        Handles POST requests for creating a new user.

        In this case, this method is not allowed.

        Response codes:
        - 403 (FORBIDDEN): The method is not allowed.
        """
        return Response(
            "Method not allowed",
            status=status.HTTP_403_FORBIDDEN
        )

    @swagger_auto_schema(auto_schema=None)
    def destroy(self, request, *args, **kwargs):
        """
        Handles DELETE requests for deleting a user.

        In this case, this method is not allowed.

        Response codes:
        - 403 (FORBIDDEN): The method is not allowed.
        """
        return Response(
            "Method not allowed",
            status=status.HTTP_403_FORBIDDEN
        )

    @swagger_auto_schema(auto_schema=None)
    def update(self, request, *args, **kwargs):
        """
        Handles PUT requests for updating user information.

        In this case, this method is not allowed.

        Response codes:
        - 403 (FORBIDDEN): The method is not allowed.
        """
        return Response(
            "Method not allowed",
            status=status.HTTP_403_FORBIDDEN
        )

    @swagger_auto_schema(
        responses={200: UserPatchSerializer()},
        operation_id='partial update'
    )
    def partial_update(self, request, *args, **kwargs):
        """
        Handles PATCH requests for partially updating user information.

        If the data is valid, user information is updated.

        Response codes:
        - 200 (OK): User information is successfully updated.
        - 400 (BAD REQUEST): Provided data is not valid.
        """
        instance = self.get_object()
        data = request.data

        serializer = UserPatchSerializer(instance, data=data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
