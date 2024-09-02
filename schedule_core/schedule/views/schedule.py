from rest_framework import viewsets, permissions
from rest_framework import parsers

from schedule.models import Schedule
from schedule_core.swagger_service.apply_swagger_auto_schema import apply_swagger_auto_schema
from schedule.serializers import ScheduleSerializer
from users.permissions import IsBlocked


class ScheduleViewSet(viewsets.ModelViewSet):
    serializer_class = ScheduleSerializer
    permission_classes = [permissions.IsAuthenticated, IsBlocked]
    parser_classes = [parsers.MultiPartParser, ]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            queryset = (
                self.request.user.user_schedules
                .select_related('category')
                .only('id', 'title', 'description', 'due_date', 'category__name')
            )

            return queryset

        return Schedule.objects.none()


ScheduleViewSet = apply_swagger_auto_schema(
    tags=['schedule'], excluded_methods=[]
)(ScheduleViewSet)
