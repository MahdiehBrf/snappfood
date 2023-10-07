from datetime import timezone, datetime

from django.db import models, transaction

from .delay_report_check import DelayReportCheck
from ..services import re_estimate_delivery_hour


class DelayReport(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    delay = models.PositiveIntegerField()
    new_delivery_at = models.DateTimeField(null=True, blank=True)
    order = models.ForeignKey("order.Order", related_name="delay_reports",
                              on_delete=models.deletion.CASCADE)
    # user

    def calculate_delay(self):
        self.delay = (datetime.now(timezone.utc) - self.order.delivery_at).total_seconds()

    @transaction.atomic
    def update_order_delivery_at(self):
        new_estimation_hour = re_estimate_delivery_hour()
        new_estimation = self.order.delivery_at.replace(hour=new_estimation_hour,
                                                        minute=0, second=0, microsecond=0)
        self.order.update_delivery_at(new_estimation)
        self.new_delivery_at = new_estimation
        self.save()

    def create_check(self):
        DelayReportCheck.objects.create_for(order_id=self.order_id, delay_report_id=self.id)
