from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.viewsets import GenericViewSet

from order.api.permissions import IsAgentFree
from order.models import DelayReportCheck


class DelayReportCheckViewSet(GenericViewSet):
    queryset = DelayReportCheck.objects.all()
    # permission_classes = [agent]

    def permission_denied(self, request, message=None, code=None):
        if not message:
            super().permission_denied(request, message, code)
        raise PermissionDenied(detail=message, code=code)

    @action(
        methods=["POST"],
        detail=False,
        permission_classes=[IsAgentFree, ]
    )
    def assign(self, request, *args, **kwargs):
        # agent_id = self.request.user.id
        agent_id = int(request.data.get("agent_id"))
        success = DelayReportCheck.objects.find_and_assign_to(agent_id)
        return Response(status=HTTP_200_OK, data={"success": success})
