from celery import shared_task


@shared_task(acks_late=True)
def create_check_for(order_id: int, delay_report_id: int):
    from order.models import DelayReportCheck
    DelayReportCheck.objects.create_for(order_id=order_id, delay_report_id=delay_report_id)
