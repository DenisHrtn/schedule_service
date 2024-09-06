from rest_framework import serializers
from schedule.models.history import History


class HistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = History
        fields = ['changes', 'changed_at']
