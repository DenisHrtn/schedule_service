from rest_framework import serializers

from users.models import User
from users.models.profile import Profile
from users.services.email_service import EmailService


class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True)
    password_confirmation = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('email', 'password', 'password_confirmation',)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        password_confirmation = attrs.get('password_confirmation')

        if password != password_confirmation:
            raise serializers.ValidationError("Passwords mismatch")

        if not all([email, password, password_confirmation]):
            raise serializers.ValidationError("All fields are required")

        if User.objects.filter(email=email, code=None).exists():
            raise serializers.ValidationError("User with this email already registered")

        if User.objects.filter(email=email, code__isnull=False).exists():
            raise serializers.ValidationError("The user has completed the first stage of registration,"
                                              " confirm the code sent to your email.")

        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(
            password=validated_data['password'],
            email=validated_data['email'],
        )

        sender_service = EmailService()

        sender_service.send_code_to_email(email=validated_data['email'])

        Profile.objects.create(user=user)

        return user