from rest_framework import serializers

from schedule.models import Comment


class CommentsSerializer(serializers.ModelSerializer):
    model = Comment
    fields = ['text', 'created_at']
