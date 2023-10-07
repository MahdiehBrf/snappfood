from rest_framework import serializers

from order.models import DelayReport, Order


class DelayReportCreateSerializer(serializers.ModelSerializer):

    def to_internal_value(self, data):
        data["order_id"] = self.context["view"].kwargs["order_id"]
        return data

    class Meta:
        model = DelayReport
        fields = ["order_id", "delay", "created_at", "new_delivery_at"]
        read_only_fields = ["delay", "created_at", "new_delivery_at"]
