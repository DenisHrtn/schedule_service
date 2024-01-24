from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.parsers import MultiPartParser
from django.contrib.auth import get_user_model
from rest_framework import generics

from users.serializers.register_serializer import RegisterSerializer


User = get_user_model()


class RegistrationAPIView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        confirm_password = request.data.get('confirm_password')

        if not all([email, password, confirm_password]):
            return Response("All fields are required", status=400)

        if User.objects.filter(email=email, code=None).exists():
            return Response(
                'User with that email already registered',
                status=status.HTTP_400_BAD_REQUEST
            )

        if User.objects.filter(email=email, code__isnull=False).exists():
            return Response(
                'The user has completed the first stage of registration, confirm the code sent to your email.',
                status=status.HTTP_400_BAD_REQUEST
            )

        if password and password != confirm_password:
            return Response("Password mismatch", status=400)

        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Code has been send"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)