from django.db.models.signals import pre_save
from django.dispatch import receiver

from order.models import DelayReport


@receiver(pre_save, sender=DelayReport)
def income_change_log_pre_save(sender, instance, **kwargs):
    if not instance.pk:
        instance.calculate_delay()
