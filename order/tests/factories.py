import random
from datetime import timedelta

import factory
from django.utils import timezone
from factory.django import DjangoModelFactory

from order.models import DelayReport, Order
from vendor.tests.factories import VendorFactory


class DelayReportFactory(DjangoModelFactory):
    class Meta:
        model = DelayReport

    name = factory.Sequence(lambda n: f"courier{n}")


class OrderFactory(DjangoModelFactory):
    class Meta:
        model = Order


    vendor = factory.SubFactory(VendorFactory)
    created_at = factory.LazyAttribute(lambda _: timezone.now())
    submitted_at = factory.LazyAttribute(lambda obj: obj.created_at + timedelta(minutes=random.randint(0, 10)))
    delivery_at = factory.LazyAttribute(lambda obj: obj.created_at + timedelta(minutes=random.randint(0, 59)))
