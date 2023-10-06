from django.db import models


class DelayReport(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    delay = models.PositiveIntegerField()
    order = models.ForeignKey("order.Order", related_name="delay_reports",
                              on_delete=models.deletion.CASCADE)
    # user

