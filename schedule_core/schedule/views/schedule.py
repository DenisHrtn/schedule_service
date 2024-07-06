from rest_framework import viewsets, permissions
from rest_framework import parsers

from schedule_core.swagger_service.apply_swagger_auto_schema import apply_swagger_auto_schema
from schedule.serializers import ScheduleSerializer
from users.permissions import IsBlocked


class ScheduleViewSet(viewsets.ModelViewSet):
    serializer_class = ScheduleSerializer
    permission_classes = [permissions.AllowAny, IsBlocked]
    parser_classes = [parsers.MultiPartParser, ]

    def get_queryset(self):
        return self.request.user.schedules_users.select_related('category', 'mark')


ScheduleViewSet = apply_swagger_auto_schema(
    tags=['schedule'], excluded_methods=[]
)(ScheduleViewSet)
