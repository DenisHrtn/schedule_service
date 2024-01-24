from rest_framework import serializers
from django.contrib.auth import get_user_model

from users.models import User
from users.models.profile import Profile


class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True)
    password_confirmation = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('email', 'password', 'password_confirmation',)

    def create(self, validated_data):
        user = User.objects.create_user(
            password=validated_data['password'],
            email=validated_data.get['email', ''],
        )

        Profile.objects.create(user=user)

        return user