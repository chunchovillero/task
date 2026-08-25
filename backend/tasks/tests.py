from django.test import TestCase, override_settings
from rest_framework.test import APIClient

from .models import Task


class TaskApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    @override_settings(AI_FAKE_MODE=True)
    def test_analyze_marks_task_as_urgent(self):
        task = Task.objects.create(
            titulo="Enviar propuesta hoy",
            descripcion="La propuesta debe enviarse antes de las 18 horas.",
        )

        response = self.client.post(f"/api/tasks/{task.id}/analyze/")

        self.assertEqual(response.status_code, 200)
        task.refresh_from_db()
        self.assertEqual(task.categoria, Task.Category.URGENTE)

    @override_settings(AI_FAKE_MODE=True)
    def test_analyze_marks_task_as_not_urgent(self):
        task = Task.objects.create(
            titulo="Ordenar documentos",
            descripcion="Organizar las carpetas del archivo personal.",
        )

        response = self.client.post(f"/api/tasks/{task.id}/analyze/")

        self.assertEqual(response.status_code, 200)
        task.refresh_from_db()
        self.assertEqual(task.categoria, Task.Category.NO_URGENTE)
