from rest_framework import serializers
from django.contrib.auth.hashers import check_password
from django.db.models import Q
from django.contrib.auth import get_user_model

User = get_user_model()


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('email', 'password')

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        user = User.objects.filter(Q(email=email)).first()
        if not user:
            raise serializers.ValidationError("Invalid login credentials")
        if not check_password(password, user.password):
            raise serializers.ValidationError("Invalid password credentials")
        attrs['user'] = user
        return attrs