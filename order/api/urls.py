from rest_framework.routers import DefaultRouter

from .views import OrderDelayReportViewSet
from .views.delay_report_check_views import DelayReportCheckViewSet

order_router = DefaultRouter()

order_delay_report_router = DefaultRouter()
order_delay_report_router.register("orders/(?P<order_id>[0-9]+)/delays",
                                   OrderDelayReportViewSet, basename="order-delays")
order_router.registry.extend(order_delay_report_router.registry)

delay_report_check_router = DefaultRouter()
delay_report_check_router.register("orders/checks",
                                   DelayReportCheckViewSet, basename="checks")
order_router.registry.extend(delay_report_check_router.registry)
