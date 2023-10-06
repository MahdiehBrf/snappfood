from rest_framework import serializers

from order.models import DelayReport, Order


class OrderDeliverySerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = ["id", "delivery_at"]
        read_only_fields = fields


class DelayReportCreateSerializer(serializers.ModelSerializer):
    order = OrderDeliverySerializer()

    def to_internal_value(self, data):
        data["order_id"] = self.context["view"].kwargs["order_id"]
        return data

    class Meta:
        model = DelayReport
        fields = ["order", "delay", "created_at"]
        read_only_fields = ["delay", "created_at"]
