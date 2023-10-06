from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from order.api.serializers.serializers import DelayReportCreateSerializer
from order.models import DelayReport, Trip


class DelayReportViewSet(mixins.CreateModelMixin, GenericViewSet):
    queryset = DelayReport.objects.all()
    # permission_classes = [user]

    def perform_create(self, serializer):
        super().perform_create(serializer)
        try:
            trip_state = serializer.instance.order.trip.state
        except Trip.DoesNotExist:
            trip_state = None
        if trip_state in [Trip.State.ASSIGNED, Trip.State.AT_VENDOR, Trip.State.PICKED]:
            serializer.instance.update_order_delivery_at()
        else:
            serializer.instance.create_check()

    def create(self, request, *args, **kwargs):
        self.serializer_class = DelayReportCreateSerializer
        return super().create(request, *args, **kwargs)
