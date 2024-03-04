from rest_framework.response import Response
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.parsers import MultiPartParser

from users.serializers.verification_serializer import VerificationSerializer
from users.permissions.is_blocked import IsBlocked
from schedule_core.swagger_service.apply_swagger_auto_schema import apply_swagger_auto_schema


class VerificationView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated, IsBlocked]
    serializer_class = VerificationSerializer
    parser_classes = [MultiPartParser]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if serializer.is_valid():
            serializer.save()
            return Response(
                "Your verification message has been sent to your email address. Verification successfully.",
                status=status.HTTP_201_CREATED
            )
        return Response(
            "Something went wrong. Please try again.",
            status=status.HTTP_400_BAD_REQUEST
        )


VerificationView = apply_swagger_auto_schema(
    tags=['verification'], excluded_methods=[]
)(VerificationView)