from django.db import IntegrityError
from rest_framework.test import APIClient
from django.test import TestCase

from agent.tests.factories import AgentFactory
from order.models import DelayReport, DelayReportCheck
from order.tests.factories import OrderFactory


class DelayReportCheckModelTest(TestCase):

    def test_create_for_order(self):
        order = OrderFactory()
        report = DelayReport.objects.create(order=order)
        self.assertEquals(DelayReportCheck.objects.count(), 0)
        DelayReportCheck.objects.create_for(order.id, report.id)
        check = DelayReportCheck.objects.first()
        self.assertNotEquals(check, None)
        self.assertEquals(check.order_id, order.id)
        self.assertEquals(check.delay_report_id, report.id)
        self.assertEquals(check.agent_id, None)
        self.assertEquals(check.state, DelayReportCheck.State.UNASSIGNED)

    def test_create_for_order_with_unchecked_check(self):
        order = OrderFactory()
        report = DelayReport.objects.create(order=order)
        DelayReportCheck.objects.create_for(order.id, report.id)
        self.assertEquals(DelayReportCheck.objects.count(), 1)
        report2 = DelayReport.objects.create(order=order)
        DelayReportCheck.objects.create_for(order.id, report2.id)
        self.assertEquals(DelayReportCheck.objects.count(), 1)

    def test_create_for_order_with_checked_check(self):
        order = OrderFactory()
        report = DelayReport.objects.create(order=order)
        DelayReportCheck.objects.create_for(order.id, report.id)
        check = DelayReportCheck.objects.first()
        self.assertNotEquals(check, None)
        check.state = DelayReportCheck.State.CHECKED
        check.save()
        report2 = DelayReport.objects.create(order=order)
        DelayReportCheck.objects.create_for(order.id, report2.id)
        self.assertEquals(DelayReportCheck.objects.count(), 2)

    def test_find_and_assign_to_agent(self):
        agent1 = AgentFactory()
        reports = []
        for _ in range(10):
            order = OrderFactory()
            report = DelayReport.objects.create(order=order)
            DelayReportCheck.objects.create_for(order.id, report.id)
            check = report.delay_check
            check.state = DelayReportCheck.State.CHECKED
            check.agent_id = agent1.id
            check.save()
            report2 = DelayReport.objects.create(order=order)
            DelayReportCheck.objects.create_for(order.id, report2.id)
            reports.append(report2)
        agent2 = AgentFactory()
        found, check = DelayReportCheck.objects.find_and_assign_to(agent2.id)
        self.assertEquals(found, True)
        self.assertEquals(check.delay_report_id, reports[0].id)
        agent3 = AgentFactory()
        found, check = DelayReportCheck.objects.find_and_assign_to(agent3.id)
        self.assertEquals(found, True)
        self.assertEquals(check.delay_report_id, reports[1].id)

    def test_create_with_order_with_unchecked_check(self):
        order = OrderFactory()
        report = DelayReport.objects.create(order=order)
        DelayReportCheck.objects.create(order=order, delay_report=report)
        self.assertEquals(DelayReportCheck.objects.count(), 1)
        report2 = DelayReport.objects.create(order=order)
        self.assertRaises(IntegrityError,
                          DelayReportCheck.objects.create(order=order, delay_report=report2))


class DelayReportCheckViewTest(TestCase):
    def test_assign_check(self):
        order = OrderFactory()
        report = DelayReport.objects.create(order=order)
        DelayReportCheck.objects.create_for(order.id, report.id)
        agent = AgentFactory()
        client = APIClient()
        response = client.post(f"/api/v1/orders/checks/assign/", data={"agent_id": agent.id})
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEquals(response_data['success'], True)

    def test_assign_check_to_agent_with_checked(self):
        agent = AgentFactory()
        order = OrderFactory()
        report = DelayReport.objects.create(order=order)
        DelayReportCheck.objects.create_for(order.id, report.id)
        check = report.delay_check
        check.state = DelayReportCheck.State.CHECKED
        check.agent_id = agent.id
        check.save()
        order2 = OrderFactory()
        report2 = DelayReport.objects.create(order=order2)
        DelayReportCheck.objects.create_for(order2.id, report2.id)
        client = APIClient()
        response = client.post(f"/api/v1/orders/checks/assign/", data={"agent_id": agent.id})
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEquals(response_data['success'], True)

    def test_assign_check_to_agent_with_unchecked(self):
        agent = AgentFactory()
        order = OrderFactory()
        report = DelayReport.objects.create(order=order)
        DelayReportCheck.objects.create_for(order.id, report.id)
        DelayReportCheck.objects.find_and_assign_to(agent.id)
        order2 = OrderFactory()
        report2 = DelayReport.objects.create(order=order2)
        DelayReportCheck.objects.create_for(order2.id, report2.id)
        client = APIClient()
        response = client.post(f"/api/v1/orders/checks/assign/", data={"agent_id": agent.id})
        self.assertEqual(response.status_code, 403)
