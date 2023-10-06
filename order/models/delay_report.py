from datetime import timezone, datetime

from django.db import models

from .delay_report_check import DelayReportCheck
from ..services import re_estimate_delivery_hour


class DelayReport(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    delay = models.PositiveIntegerField()
    order = models.ForeignKey("order.Order", related_name="delay_reports",
                              on_delete=models.deletion.CASCADE)
    # user

    def calculate_delay(self):
        self.delay = (datetime.now(timezone.utc) - self.order.delivery_at).total_seconds()

    def update_order_delivery_at(self):
        new_estimation_hour = re_estimate_delivery_hour()
        self.order.update_delivery_at_hour(new_estimation_hour)

    def create_check(self):
        DelayReportCheck.objects.create_for(order_id=self.order_id, delay_report_id=self.id)
