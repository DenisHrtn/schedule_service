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
        read_only_fields = ['date_joined', 'is_verified']

    def get_profile(self, obj):
        profile = Profile.objects.get(user=obj)
        serializer = None
        serializer = ProfileSerializer(profile)
        return serializer.data


class UserPatchSerializer(serializers.Serializer):
    email = serializers.EmailField(required=False)
    username = serializers.CharField(required=False, max_length=25)

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.username = validated_data.get('username', instance.username)
        instance.save()
        return instance
