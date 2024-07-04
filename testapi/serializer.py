from rest_framework import serializers


class TestSerializer(serializers.Serializer):
    visitor_name = serializers.CharField(max_length=100)
