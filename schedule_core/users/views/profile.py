from rest_framework import status, permissions
from rest_framework import viewsets
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema

from users.serializers.profile_serializer import ProfileSerializer, ProfileUpdateSerializer
from users.models import User, Profile
from users.permissions.is_blocked import IsBlocked


class ProfileViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing user profiles.

    This ViewSet allows authenticated users to view, create, update, and delete their profiles.
    Superusers have additional permissions to view all profiles.

    Parameters:
        - permission_classes ([IsBlocked, permissions.IsAuthenticated]):
            Permission classes for accessing this viewset.
            Authenticated users are required, and blocked users are not allowed.

        - serializer_class (ProfileSerializer):
            Serializer for profile data.
            It handles validation and serialization of profile information.

    Methods:
        - get_queryset():
            Returns the queryset of profiles that the user has permission to access.
            Superusers can view all profiles, while regular users can only view their own profile.

        - create(request):
            Handles requests for creating a new profile.
            This method is not allowed and will return a "Method Not Allowed" response code.

        - update(request):
            Handles requests for updating the profile.
            This method is not allowed and will return a "Method Not Allowed" response code.

        - destroy(request):
            Handles requests for deleting the profile.
            This method is not allowed and will return a "Method Not Allowed" response code.

        - partial_update(request):
            Handles requests for partially updating the profile.
            It allows users to update specific fields in their profile.
            If the provided data is valid, the profile will be updated and a "200 OK" response will be returned.
            If the data is invalid, a "400 Bad Request" response will be returned along with validation errors.
    """
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
        """
        Method not allowed.

        Creating a new profile is not allowed.
        """
        return Response(
            "Method Not Allowed",
            status=status.HTTP_403_FORBIDDEN
        )

    @swagger_auto_schema(auto_schema=None)
    def update(self, request, *args, **kwargs):
        """
        Method not allowed.

        Updating the profile is not allowed.
        """
        return Response(
            "Method Not Allowed",
            status=status.HTTP_403_FORBIDDEN
        )

    @swagger_auto_schema(auto_schema=None)
    def destroy(self, request, *args, **kwargs):
        """
        Method not allowed.

        Deleting the profile is not allowed.
        """
        return Response(
            "Method Not Allowed",
            status=status.HTTP_403_FORBIDDEN
        )

    @swagger_auto_schema(
        responses={200: ProfileUpdateSerializer()},
        operation_id='update_profile'
    )
    def partial_update(self, request, *args, **kwargs):
        """
        Update profile fields partially.

        Update specific fields in the user's profile.
        If the provided data is valid, the profile will be updated and a "200 OK" response will be returned.
        If the data is invalid, a "400 Bad Request" response will be returned along with validation errors.
        """
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