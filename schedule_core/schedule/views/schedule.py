from rest_framework import viewsets, permissions, status
from rest_framework import parsers
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response

from schedule_core.swagger_service.apply_swagger_auto_schema import apply_swagger_auto_schema
from schedule.serializers import ScheduleSerializer
from users.permissions import IsBlocked


class ScheduleViewSet(viewsets.ModelViewSet):
    serializer_class = ScheduleSerializer
    permission_classes = [permissions.AllowAny, IsBlocked]
    parser_classes = [parsers.MultiPartParser, ]

    def get_queryset(self):
        return self.request.user.schedules_users.select_related('category', 'mark').defer('user')

    # @swagger_auto_schema(auto_schema=None)
    # def update(self, request, *args, **kwargs):
    #     return Response("Method Not Allowed", status.HTTP_405_METHOD_NOT_ALLOWED)

    # @swagger_auto_schema(request_body=ScheduleSerializer)
    # def partial_update(self, request, *args, **kwargs):
    #     return super().partial_update(request, *args, **kwargs)


ScheduleViewSet = apply_swagger_auto_schema(
    tags=['schedule'], excluded_methods=[]
)(ScheduleViewSet)
