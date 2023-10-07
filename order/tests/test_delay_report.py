from datetime import datetime, timedelta
from unittest.mock import patch

from rest_framework.test import APIClient
from django.test import TestCase
from django.utils import timezone

from order.models import DelayReport, DelayReportCheck, Trip
from order.tests.factories import OrderFactory
from vendor.models import DailyDelay


class FakeDateTime(datetime):
    """ A fake replacement for datetime that can be mocked for testing."""
    def __new__(cls, old, *args, **kwargs):
        return super().__new__(cls, old.year, old.month, old.day, old.hour, old.minute, old.second)


class DelayReportModelTest(TestCase):

    def test_delay_calculation(self):
        april_1 = datetime(2023, 9, 1, 13, 30).replace(tzinfo=timezone.get_default_timezone())
        fake_april_1 = FakeDateTime(april_1).replace(tzinfo=timezone.get_default_timezone())
        order = OrderFactory(delivery_at=april_1 - timedelta(minutes=1))
        with patch.object(timezone, 'now', return_value=fake_april_1):
            report = DelayReport.objects.create(order=order)
            self.assertEquals(report.delay, 60)

    @patch('order.services.re_estimate_delivery_hour',
           return_value={"status": True, "data": {"eta": 14}})
    def test_update_order_delivery_at(self, mock):
        april_1 = datetime(2023, 9, 1, 13, 30).replace(tzinfo=timezone.get_default_timezone())
        fake_april_1 = FakeDateTime(april_1).replace(tzinfo=timezone.get_default_timezone())
        order = OrderFactory(delivery_at=april_1 - timedelta(minutes=1))
        with patch.object(timezone, 'now', return_value=fake_april_1):
            report = DelayReport.objects.create(order=order)
            report.update_order_delivery_at()
            new_estimation = datetime(2023, 9, 1, 14, 00).replace(tzinfo=timezone.get_default_timezone())
            self.assertEquals(report.new_delivery_at, new_estimation)
            self.assertEquals(report.order.delivery_at, new_estimation)

    @patch('order.services.re_estimate_delivery_hour',
           return_value={"status": True, "data": {"eta": 14}})
    @patch('order.models.Order.update_delivery_at', side_effect=Exception())
    def test_rollback_update_order_delivery_at(self, mock, mock2):
        april_1 = datetime(2023, 9, 1, 13, 30).replace(tzinfo=timezone.get_default_timezone())
        fake_april_1 = FakeDateTime(april_1).replace(tzinfo=timezone.get_default_timezone())
        order = OrderFactory(delivery_at=april_1 - timedelta(minutes=1))
        with patch.object(timezone, 'now', return_value=fake_april_1):
            report = DelayReport.objects.create(order=order)
            try:
                report.update_order_delivery_at()
            except Exception:
                pass
            self.assertEquals(report.new_delivery_at, fake_april_1)
            self.assertEquals(report.order.delivery_at, april_1 - timedelta(minutes=1))

    def test_delay_creation(self):
        april_1 = datetime(2023, 9, 1, 13, 30).replace(tzinfo=timezone.get_default_timezone())
        fake_april_1 = FakeDateTime(april_1).replace(tzinfo=timezone.get_default_timezone())
        order = OrderFactory(delivery_at=april_1 - timedelta(minutes=1))
        with patch.object(timezone, 'now', return_value=fake_april_1):
            report = DelayReport.objects.create(order=order)
            self.assertEquals(report.delay, 60)
            daily_delay = DailyDelay.objects.first()
            self.assertNotEquals(daily_delay, None)
            self.assertEquals(daily_delay.vendor_id, report.order.vendor_id)
            self.assertEquals(daily_delay.value, report.delay)
            self.assertEquals(daily_delay.date, fake_april_1.date())


class DelayReportViewTest(TestCase):

    def test_delay_report_create_without_trip(self):
        client = APIClient()
        april_1 = datetime(2023, 9, 1, 13, 30).replace(tzinfo=timezone.get_default_timezone())
        fake_april_1 = FakeDateTime(april_1).replace(tzinfo=timezone.get_default_timezone())
        order = OrderFactory(delivery_at=april_1 - timedelta(minutes=1))
        with patch.object(timezone, 'now', return_value=fake_april_1):
            response = client.post(f"/api/v1/orders/{order.id}/delays/")
            self.assertEqual(response.status_code, 201)
            report = DelayReport.objects.first()
            self.assertNotEquals(report, None)
            self.assertEquals(report.delay, 60)
            daily_delay = DailyDelay.objects.first()
            self.assertNotEquals(daily_delay, None)
            self.assertEquals(daily_delay.vendor_id, report.order.vendor_id)
            self.assertEquals(daily_delay.value, report.delay)
            self.assertEquals(daily_delay.date, fake_april_1.date())
            check = DelayReportCheck.objects.first()
            self.assertNotEquals(check, None)
            self.assertEquals(check.delay_report_id, report.id)
            self.assertEquals(check.order_id, report.order_id)
            self.assertEquals(check.agent_id, None)
            self.assertEquals(check.state, DelayReportCheck.State.UNASSIGNED)

    @patch('order.services.re_estimate_delivery_hour',
           return_value={"status": True, "data": {"eta": 14}})
    def test_delay_report_create_with_trip(self, mock):
        client = APIClient()
        april_1 = datetime(2023, 9, 1, 13, 30).replace(tzinfo=timezone.get_default_timezone())
        fake_april_1 = FakeDateTime(april_1).replace(tzinfo=timezone.get_default_timezone())
        order = OrderFactory(delivery_at=april_1 - timedelta(minutes=1))
        Trip.objects.create(order=order)
        with patch.object(timezone, 'now', return_value=fake_april_1):
            response = client.post(f"/api/v1/orders/{order.id}/delays/")
            self.assertEqual(response.status_code, 201)
            report = DelayReport.objects.first()
            self.assertNotEquals(report, None)
            self.assertEquals(report.delay, 60)
            new_estimation = datetime(2023, 9, 1, 14, 00).replace(
                tzinfo=timezone.get_default_timezone())
            self.assertEquals(report.new_delivery_at, new_estimation)
            self.assertEquals(report.order.delivery_at, new_estimation)
            daily_delay = DailyDelay.objects.first()
            self.assertNotEquals(daily_delay, None)
            self.assertEquals(daily_delay.vendor_id, report.order.vendor_id)
            self.assertEquals(daily_delay.value, report.delay)
            self.assertEquals(daily_delay.date, fake_april_1.date())
