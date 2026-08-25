import logging

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Task
from .serializers import TaskSerializer
from .services.urgency_agent import AgentConfigurationError, analyze_urgency


logger = logging.getLogger(__name__)


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all().order_by("-created_at")
    serializer_class = TaskSerializer

    @action(detail=True, methods=["post"])
    def analyze(self, request, pk=None):
        task = self.get_object()

        try:
            analysis = analyze_urgency(task.title, task.description)
        except AgentConfigurationError as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        except Exception:
            logger.exception("No fue posible analizar la urgencia de la tarea %s", task.pk)
            return Response(
                {"detail": "El proveedor de IA no pudo analizar la tarea."},
                status=status.HTTP_502_BAD_GATEWAY,
            )

        task.category = (
            Task.Category.URGENT if analysis.urgent else Task.Category.NOT_URGENT
        )
        task.save(update_fields=["category"])
        return Response(self.get_serializer(task).data)
