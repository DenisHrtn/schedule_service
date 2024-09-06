from rest_framework import serializers
import datetime
import json

from schedule.models import Schedule, Category
from schedule.models.history import History
from schedule.serializers.history_serializer import HistorySerializer
from schedule.serializers.comments_serializer import CommentsSerializer


class ScheduleSerializer(serializers.ModelSerializer):
    history = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()

    class Meta:
        model = Schedule
        fields = [
            'title',
            'description',
            'due_date',
            'category',
            'mark',
            'completed',
            'created_at',
            'updated_at',
            'history',
            'comments',
        ]

    def get_history(self, obj):
        history = obj.history.all()
        serializer = HistorySerializer(history, many=True)
        return serializer.data

    def get_comments(self, obj):
        comments = obj.comments.all()
        serializer = CommentsSerializer(comments, many=True)
        return serializer.data

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

        def custom_serializer(obj):
            if isinstance(obj, (datetime.date, datetime.datetime)):
                return obj.isoformat()
            if isinstance(obj, Category):
                return str(obj)
            raise TypeError(f"Type {type(obj)} not serializable")

        History.objects.create(
            schedule=instance,
            changed_at=instance.updated_at,
            changes=json.dumps(
                [instance.title, instance.due_date, instance.description,
                 instance.category, instance.mark, instance.completed],
                default=custom_serializer
            )
        )

        return instance
