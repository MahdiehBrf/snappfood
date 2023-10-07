from django.db import models, transaction
from django.utils import timezone

from ..tasks import create_check_for
from ..services import re_estimate_delivery_hour


class DelayReport(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    delay = models.PositiveIntegerField()
    new_delivery_at = models.DateTimeField(null=True, blank=True)
    order = models.ForeignKey("order.Order", related_name="delay_reports",
                              on_delete=models.deletion.CASCADE)
    # user

    def calculate_delay(self):
        self.delay = (timezone.now() - self.order.delivery_at).total_seconds()

    @transaction.atomic
    def update_order_delivery_at(self):
        new_estimation_hour = re_estimate_delivery_hour()
        new_estimation = self.order.delivery_at.replace(hour=new_estimation_hour,
                                                        minute=0, second=0, microsecond=0)
        self.new_delivery_at = new_estimation
        self.save()
        self.order.update_delivery_at(new_estimation)

    def create_check(self):
        create_check_for.delay(order_id=self.order_id, delay_report_id=self.id)
