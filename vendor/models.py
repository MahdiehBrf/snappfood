from django.db import models
from django.db.models import Max, Sum
from django.utils import timezone

from order.models import DelayReport


class Vendor(models.Model):
    pass


class DailyDelayManager(models.Manager):
    def update_or_create_for(self, vendor_id: int):
        queryset = self.get_queryset()
        today = timezone.now().date()
        reports = DelayReport.objects.filter(created_at__date=today, order__vendor_id=vendor_id)
        value = reports.values('order_id', 'new_delivery_at').annotate(Max('delay')).\
            aggregate(Sum('delay__max'))['delay__max__sum']
        return queryset.update_or_create(vendor_id=vendor_id, date=today,
                                         defaults={"value": value})


class DailyDelay(models.Model):
    vendor = models.ForeignKey("vendor.Vendor", related_name="daily_delays",
                               on_delete=models.deletion.CASCADE)
    date = models.DateField(db_index=True)
    value = models.PositiveIntegerField()

    objects = DailyDelayManager()

    class Meta:
        unique_together = ["date", "vendor"]
