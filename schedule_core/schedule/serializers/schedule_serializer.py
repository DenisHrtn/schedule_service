from rest_framework import serializers
import datetime

from schedule.models import Schedule


class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        exclude = ['user', ]

    def create(self, validated_data):
        if Schedule.objects.filter(user=self.context['request'].user, title=validated_data['title']).exists():
            raise serializers.ValidationError({'title': 'This title is already in use.'})

        if validated_data['due_date'] and validated_data['due_date'] < datetime.date.today():
            raise serializers.ValidationError({'due_date': 'Date cannot be in the future.'})

        schedule = Schedule.objects.create(user=self.context['request'].user,**validated_data)
        return schedule
