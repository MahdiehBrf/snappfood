from typing import Optional

from django.db import models, IntegrityError, transaction


class DelayReportCheckManager(models.Manager):
    def create_for(self, order_id: int, delay_report_id: int) -> bool:
        queryset = self.get_queryset()
        self._for_write = True
        has_unchecked = queryset.filter(order_id=order_id).exclude(state=DelayReportCheck.State.CHECKED).exists()
        if has_unchecked:
            return False
        try:
            self.create(order_id=order_id, delay_report_id=delay_report_id)
            return True
        except IntegrityError:
            return False

    def find_and_assign_to(self, agent_id: int) -> (bool, Optional[int]):
        queryset = self.get_queryset()
        with transaction.atomic(using=self.db):
            obj = queryset.select_for_update().filter(agent_id=None).first()
            if not obj:
                return False, None
            obj.agent_id = agent_id
            obj.save(update_fields=["agent_id"])
        return True, obj


class DelayReportCheck(models.Model):
    class State(models.IntegerChoices):
        UNASSIGNED = 0
        ASSIGNED = 1
        CHECKED = 2
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    order = models.ForeignKey("order.Order", related_name="delay_report_checks",
                              on_delete=models.deletion.CASCADE)
    agent = models.ForeignKey("agent.Agent", related_name="delay_report_checks",
                              on_delete=models.deletion.SET_NULL, null=True)
    delay_report = models.OneToOneField("order.DelayReport", related_name="delay_check",
                                        on_delete=models.deletion.CASCADE)

    state = models.IntegerField(choices=State.choices, default=State.UNASSIGNED)
    # user

    objects = DelayReportCheckManager()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["order"],
                name="%(app_label)s_%(class)s_unique_unchecked_order",
                condition=models.Q(state__lte=1),
            )
        ]
        ordering = ['created_at', ]
