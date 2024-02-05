from rest_framework import serializers

from users.models import User


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def validate(self, attrs):
        email = attrs.get('email')
        if not email:
            raise serializers.ValidationError("Email is required")
        if not User.objects.filter(email=email):
            raise serializers.ValidationError("User not found")
        return attrs