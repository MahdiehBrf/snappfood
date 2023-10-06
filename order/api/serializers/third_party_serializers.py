from rest_framework import serializers


class DataMockResponseSerializer(serializers.Serializer):
    eta = serializers.IntegerField(min_value=0, max_value=24)

    class Meta:
        fields = ["eta"]


class MockResponseSerializer(serializers.Serializer):
    status = serializers.BooleanField()
    data = DataMockResponseSerializer()

    class Meta:
        fields = ["status", "data"]
