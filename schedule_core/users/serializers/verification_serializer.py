from rest_framework import serializers
from django.utils import timezone

from users.models.user import User
from users.models.profile import Profile
from users.services.email_service import EmailService


class VerificationSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def validate(self, attrs):
        email = attrs.get('email')
        user = User.objects.get(email=email)
        profile = Profile.objects.get(user=user)
        if not profile.country or not profile.use_service_for or not profile.city:
            raise serializers.ValidationError("Please give full information about your location and service for your")
        MIN_DAYS = 7  # minimum days to complete verification
        current_date = timezone.now()
        difference_between_dates = (current_date - profile.days_with_service).days
        if difference_between_dates < MIN_DAYS:
            raise serializers.ValidationError("You can pass verification after 7 days")
        else:
            sender_service = EmailService()
            user.is_verified = True
            user.save()
            sender_service.send_message_after_verification(email=email)

        return attrs