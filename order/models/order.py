from datetime import datetime

from django.db import models


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    submitted_at = models.DateTimeField(null=True)
    delivery_at = models.DateTimeField(null=True)
    vendor = models.ForeignKey("vendor.Vendor", related_name="orders",
                               on_delete=models.deletion.PROTECT)
    # price

    def update_delivery_at(self, value: datetime):
        self.delivery_at = value
        self.save()
