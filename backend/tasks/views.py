import logging

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Task
from .serializers import TaskSerializer
from .services.agent import AgentConfigurationError, analyze_task


logger = logging.getLogger(__name__)


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer

    def get_queryset(self):
        queryset = Task.objects.all()
        requested_status = self.request.query_params.get("status")
        if requested_status in Task.Status.values:
            queryset = queryset.filter(status=requested_status)
        return queryset

    @action(detail=True, methods=["post"])
    def analyze(self, request, pk=None):
        task = self.get_object()

        try:
            analysis = analyze_task(task.title, task.description)
        except AgentConfigurationError as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        except Exception:
            logger.exception("The AI agent could not analyze task %s", task.pk)
            return Response(
                {"detail": "El proveedor de IA no pudo analizar la tarea."},
                status=status.HTTP_502_BAD_GATEWAY,
            )

        task.category = analysis.category
        task.subtasks = analysis.subtasks
        task.save(update_fields=["category", "subtasks", "updated_at"])

        return Response(self.get_serializer(task).data)

