from rest_framework import serializers

from sites.models import Visit


class VisitAddSerializer(serializers.Serializer):
    links = serializers.ListSerializer(
        child=serializers.CharField(max_length=100)
    )

