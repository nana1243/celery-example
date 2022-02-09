from rest_framework import serializers


class CreateCalculationSerializer(serializers.BaseSerializer):
    a = serializers.IntegerField()
    b = serializers.IntegerField()

class ControlCalculationSerializer(serializers.BaseSerializer):
    task_id = serializers.CharField()