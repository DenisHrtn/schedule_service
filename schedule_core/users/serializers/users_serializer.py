from rest_framework import serializers

from users.models import User, Profile
from users.serializers import ProfileSerializer


class UserSerializer(serializers.ModelSerializer):
    profile = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'username',
            'date_joined',
            'is_verified',
            'profile',
        ]

    def get_profile(self, obj):
        profile = Profile.objects.get(user=obj)
        serializer = None
        serializer = ProfileSerializer(profile)
        return serializer.data


class UserPatchSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(required=False, partial=True)

    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'username',
            'date_joined',
            'is_verified',
            'profile',
        ]

    def update(self, instance, validated_data):
        profile_data = None
        profile = None
        profile_data = validated_data.get('profile', {})
        profile = instance.profile

        # for attr, value in profile_data.items():
        #     setattr(profile, attr, value)

        profile.save()

        return instance