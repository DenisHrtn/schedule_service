from rest_framework import serializers


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
        return attrs