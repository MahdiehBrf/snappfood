from django.db import models


class Trip(models.Model):
    class State(models.IntegerChoices):
        ASSIGNED = 0
        AT_VENDOR = 1
        PICKED = 2
        DELIVERED = 3
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    state = models.IntegerField(choices=State.choices, default=State.ASSIGNED)
    order = models.OneToOneField("order.Order", related_name="trip",
                                 on_delete=models.deletion.CASCADE)
    # courier
