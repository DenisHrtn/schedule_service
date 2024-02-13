from rest_framework import viewsets
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework import permissions, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema

from users.models.user import User
from users.serializers import UserSerializer, UserPatchSerializer
from users.permissions.is_blocked import IsBlocked


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, IsBlocked]
    serializer_class = UserSerializer

    def get_queryset(self, *args, **kwargs):
        if self.request.user.is_superuser:
            return User.objects.exclude(id=self.request.user.id)
        if self.request.user:
            return User.objects.filter(is_blocked=False, is_active=True).exclude(is_superuser=True)

    @swagger_auto_schema(auto_schema=None)
    def create(self, request, *args, **kwargs):
        return Response(
            "Method not allowed",
            status=status.HTTP_403_FORBIDDEN
        )

    @swagger_auto_schema(auto_schema=None)
    def destroy(self, request, *args, **kwargs):
        return Response(
            "Method not allowed",
            status=status.HTTP_403_FORBIDDEN
        )

    @swagger_auto_schema(auto_schema=None)
    def update(self, request, *args, **kwargs):
        return Response(
            "Method not allowed",
            status=status.HTTP_403_FORBIDDEN
        )

    @swagger_auto_schema(
        responses={200: UserSerializer()},
        operation_id='partial update'
    )
    def partial_update(self, request, *args, **kwargs):
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