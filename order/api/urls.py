from rest_framework.routers import DefaultRouter

from .views import DelayReportViewSet

order_router = DefaultRouter()

delay_report_router = DefaultRouter()
delay_report_router.register("orders/(?P<order_id>[0-9]+)/delays",
                             DelayReportViewSet, basename="delays")
order_router.registry.extend(delay_report_router.registry)
