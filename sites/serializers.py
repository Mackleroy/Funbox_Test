from rest_framework import serializers


class VisitAddSerializer(serializers.Serializer):
    links = serializers.ListSerializer(
        child=serializers.CharField(max_length=100)
    )

