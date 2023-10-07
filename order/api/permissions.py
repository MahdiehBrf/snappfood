from rest_framework.permissions import BasePermission

from order.models import DelayReportCheck


class IsAgentFree(BasePermission):
    message = 'agent is not free'

    def has_permission(self, request, view):
        agent_id = int(request.data.get("agent_id"))
        return not DelayReportCheck.objects.filter(agent_id=agent_id).exists()
