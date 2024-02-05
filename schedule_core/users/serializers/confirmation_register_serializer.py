from rest_framework import serializers


class ConfirmationRegisterSerializer(serializers.Serializer):
    code = serializers.IntegerField(required=True)
    email = serializers.EmailField(required=True)

    def validate(self, attrs):
        code = attrs.get('code')
        email = attrs.get('email')
        if not code and not email:
            raise serializers.ValidationError('Code and Email is required')
        return attrs