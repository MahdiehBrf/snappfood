from rest_framework.routers import DefaultRouter

from vendor.api.views import DelayReportViewSet

vendor_router = DefaultRouter()

daily_delays_router = DefaultRouter()
daily_delays_router.register("vendors/delays/report", DelayReportViewSet, basename="delays")
vendor_router.registry.extend(daily_delays_router.registry)

