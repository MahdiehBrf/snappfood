from django.db import models


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
    delay_report = models.ForeignKey("order.DelayReport", related_name="checks",
                                     on_delete=models.deletion.CASCADE)

    state = models.IntegerField(choices=State.choices, default=State.UNASSIGNED)
    # user

