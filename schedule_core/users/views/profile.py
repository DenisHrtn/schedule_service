from rest_framework import status, permissions
from rest_framework import viewsets
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema

from users.serializers.profile_serializer import ProfileSerializer, ProfileUpdateSerializer
from users.models import User, Profile
from users.permissions.is_blocked import IsBlocked


class ProfileViewSet(viewsets.ModelViewSet):
    permission_classes = [IsBlocked, permissions.IsAuthenticated]
    serializer_class = ProfileSerializer

    def get_queryset(self, *args, **kwargs):
        if self.request.user.is_superuser:
            return Profile.objects.select_related('user').all()
        else:
            try:
                return Profile.objects.select_related('user').filter(user_id=self.request.user.pk)
            except Profile.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(auto_schema=None)
    def create(self, request, *args, **kwargs):
        return Response(
            "Method Not Allowed",
            status=status.HTTP_403_FORBIDDEN
        )

    @swagger_auto_schema(auto_schema=None)
    def update(self, request, *args, **kwargs):
        return Response(
            "Method Not Allowed",
            status=status.HTTP_403_FORBIDDEN
        )

    @swagger_auto_schema(auto_schema=None)
    def destroy(self, request, *args, **kwargs):
        return Response(
            "Method Not Allowed",
            status=status.HTTP_403_FORBIDDEN
        )

    @swagger_auto_schema(
        responses={200: ProfileUpdateSerializer()},
        operation_id='update_profile'
    )
    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        data = request.data

        serializer = ProfileUpdateSerializer(instance, data=data, partial=True)
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