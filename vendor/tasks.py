from celery import shared_task

from vendor.models import DailyDelay


@shared_task(acks_late=True)
def create_or_update_daily_delay_for(vendor_id: int):
    DailyDelay.objects.update_or_create_for(vendor_id)
