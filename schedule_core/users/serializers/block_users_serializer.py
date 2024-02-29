from rest_framework import serializers

from users.models.user import User


class BlockUsersSerializer(serializers.Serializer):
    user_email = serializers.EmailField(required=True)
    cause = serializers.CharField(required=True, help_text="Cause of the blocking user", max_length=89)

    def validate(self, attrs):
        user_email = attrs.get('user_email')
        cause = attrs.get('cause')
        if not user_email and not cause:
            raise serializers.ValidationError("All fields are required")
        if not User.objects.filter(email=user_email).exists():
            raise serializers.ValidationError("User does not exist")

        return attrs