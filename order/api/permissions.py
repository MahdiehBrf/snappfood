from datetime import datetime, timezone

from rest_framework.generics import get_object_or_404
from rest_framework.permissions import BasePermission

from order.models import DelayReportCheck, Order


class IsAgentFree(BasePermission):
    message = "agent isn't free"

    def has_permission(self, request, view):
        agent_id = int(request.data.get("agent_id"))
        return not DelayReportCheck.objects.filter(agent_id=agent_id).exists()


class HasOrderDelay(BasePermission):
    message = "order delivery at didn't passed"

    def has_permission(self, request, view):
        order_id = view.kwargs["order_id"]
        return get_object_or_404(Order, pk=order_id).delivery_at < datetime.now(timezone.utc)
