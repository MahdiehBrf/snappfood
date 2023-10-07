from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from order.models import DelayReport
from vendor.models import DailyDelay


@receiver(pre_save, sender=DelayReport)
def income_change_log_pre_save(sender, instance, **kwargs):
    if not instance.pk:
        instance.calculate_delay()


@receiver(post_save, sender=DelayReport)
def income_change_log_post_save(sender, instance, created, **kwargs):
    if created:
        DailyDelay.objects.update_or_create_for(instance.order.vendor_id)
