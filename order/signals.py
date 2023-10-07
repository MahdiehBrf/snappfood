from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from order.models import DelayReport
from vendor.tasks import create_or_update_daily_delay_for


@receiver(pre_save, sender=DelayReport)
def income_change_log_pre_save(sender, instance, **kwargs):
    if not instance.pk:
        instance.calculate_delay()


@receiver(post_save, sender=DelayReport)
def income_change_log_post_save(sender, instance, created, **kwargs):
    if created:
        create_or_update_daily_delay_for.delay(instance.order.vendor_id)
