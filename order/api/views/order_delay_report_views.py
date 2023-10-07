from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from order.api.permissions import HasOrderDelay
from order.api.serializers.serializers import DelayReportCreateSerializer
from order.api.throttles import DelayReportThrottle
from order.models import DelayReport, Trip


class OrderDelayReportViewSet(mixins.CreateModelMixin, GenericViewSet):
    queryset = DelayReport.objects.all()
    # permission_classes = [user]
    authentication_classes = []
    throttle_classes = [DelayReportThrottle, ]

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = self.permission_classes + [HasOrderDelay, ]
        return super().get_permissions()

    def perform_create(self, serializer):
        super().perform_create(serializer)
        trip = Trip.objects.filter(order_id=serializer.instance.order.id).only('state').first()
        trip_state = trip.state if trip else None
        if trip_state in [Trip.State.ASSIGNED, Trip.State.AT_VENDOR, Trip.State.PICKED]:
            serializer.instance.update_order_delivery_at()
        else:
            serializer.instance.create_check()

    def create(self, request, *args, **kwargs):
        self.serializer_class = DelayReportCreateSerializer
        return super().create(request, *args, **kwargs)
