from rest_framework import serializers

from users.models import User
from users.services.email_service import EmailService


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def validate(self, attrs):
        email = attrs.get('email')
        if not email:
            raise serializers.ValidationError("Email is required")
        if not User.objects.filter(email=email):
            raise serializers.ValidationError("User not found")
        return attrs

    def create(self, validated_data):
        email = validated_data.get('email')
        user = User.objects.get(email=email)

        new_password = User.objects.make_random_password(length=11)
        user.set_password(new_password)
        user.save()

        sender_service = EmailService()
        subject = "Your new password"
        message = f"Your new password is {new_password}"
        sender_service.send_mail(email=email, subject=subject, message=message)

        return user