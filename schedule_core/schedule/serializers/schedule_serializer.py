from rest_framework import serializers
import datetime

from schedule.models import Schedule


class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        exclude = ['user', ]

    def create(self, validated_data):
        if Schedule.objects.filter(user=self.context['request'].user, title=validated_data['title']).exists():
            raise serializers.ValidationError({'title': "This title is already in use."})

        if validated_data['due_date'] and validated_data['due_date'] < datetime.date.today():
            raise serializers.ValidationError({'due_date': "Date cannot be in the future."})

        schedule = Schedule.objects.create(user=self.context['request'].user, **validated_data)

        return schedule

    def update(self, instance, validated_data):
        title = validated_data.get('title', instance.title)
        due_date = validated_data.get('due_date', instance.due_date)

        if Schedule.objects.filter(user=self.context['request'].user, title=title).exclude(pk=instance.pk).exists():
            raise serializers.ValidationError({'title': "This title is already in use."})

        if due_date and due_date < datetime.date.today():
            raise serializers.ValidationError({'due_date': "Date cannot be in the future."})

        if instance.completed:
            raise serializers.ValidationError({'completed': "Task is already completed."})

        instance.title = title
        instance.due_date = due_date
        instance.description = validated_data.get('description', instance.description)
        instance.category = validated_data.get('category', instance.category)
        instance.mark = validated_data.get('mark', instance.mark)
        instance.completed = validated_data.get('completed', instance.completed)
        instance.updated_at = datetime.datetime.now()
        instance.save()

        return instance
