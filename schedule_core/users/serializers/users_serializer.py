from rest_framework import serializers

from users.models import User
from users.models.profile import Profile
from users.serializers.profile_serializer import ProfileSerializer


class UserSerializer(serializers.ModelSerializer):
    profile = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'username',
            'date_joined',
            'profile',
        ]

    def get_profile(self, obj):
        profile = Profile.objects.get(user=obj)
        serializer = ProfileSerializer(profile)
        return serializer.data