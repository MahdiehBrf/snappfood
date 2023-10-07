from rest_framework import serializers


class WeaklyDelaySerializer(serializers.Serializer):
    vendor_id = serializers.IntegerField()
    value = serializers.IntegerField(min_value=0)

