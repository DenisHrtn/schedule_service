from rest_framework import generics
from rest_framework.response import Response
from rest_framework import permissions, status
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser

from users.models.user import User
from users.serializers.users_serializer import UserSerializer
from schedule_core.swagger_service.apply_swagger_auto_schema import apply_swagger_auto_schema
from users.permissions.is_blocked import IsBlocked


class UsersAPIView(generics.GenericAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, IsBlocked]
    parser_classes = [MultiPartParser, ]

    @action(methods=['GET'], detail=False)
    def get(self, request):
        if not request.user.is_authenticated:
            return Response(
                'You must be logged in to',
                status=status.HTTP_403_FORBIDDEN
            )
        else:
            users = User.objects.filter(is_blocked=False, is_active=True)
            return Response(UserSerializer(users, many=True).data)

    # TODO: Дописать энпоинты на получение конкретного пользоваетеля и фильтра по определенным пользователям
    # TODO: Написать sender service и добавить логику на активирование пользователя


UsersAPIView = apply_swagger_auto_schema(
    tags=['users'], excluded_methods=[]
)(UsersAPIView)