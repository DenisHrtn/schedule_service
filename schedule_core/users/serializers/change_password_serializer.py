from rest_framework import serializers
from django.contrib.auth.hashers import check_password

from users.models.user import User


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    new_password_confirm = serializers.CharField(required=True)

    def validate(self, attrs):
        old_password = attrs.get('old_password')
        new_password = attrs.get('new_password')
        new_password_confirm = attrs.get('new_password_confirm')
        if not old_password and not new_password and not new_password_confirm:
            raise serializers.ValidationError('All fields are required.')
        if new_password != new_password_confirm:
            raise serializers.ValidationError("Passwords are not the same")
        if not check_password(old_password, new_password):
            raise serializers.ValidationError("Your old password does not match. If you forgot it, go to recovery.")
        return attrs
