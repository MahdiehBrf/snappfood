from factory.django import DjangoModelFactory

from vendor.models import Vendor


class VendorFactory(DjangoModelFactory):
    class Meta:
        model = Vendor
