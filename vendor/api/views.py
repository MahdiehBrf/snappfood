from datetime import timedelta

from django.db.models import Sum
from django.utils import timezone
from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet

from vendor.api.serializers import WeaklyDelaySerializer
from vendor.models import DailyDelay


class DelayReportViewSet(mixins.ListModelMixin, GenericViewSet):
    queryset = DailyDelay.objects.all()
    # permission_classes = [agent]

    @action(
        methods=["GET"],
        detail=False,
        url_path='weekly'
    )
    def weekly(self, request, *args, **kwargs):
        self.serializer_class = WeaklyDelaySerializer
        today = timezone.now().date()
        days_since_saturday = (today.weekday() + 2) % 7
        previous_saturday = today - timedelta(days=days_since_saturday)
        self.queryset = self.queryset.filter(date__gte=previous_saturday).\
            values('vendor_id').annotate(value=Sum('value')).order_by('-value')
        return super().list(request, *args, **kwargs)
