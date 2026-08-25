from django.test import TestCase, override_settings
from rest_framework.test import APIClient

from .models import Task


class TaskApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_update_task_status_to_completed(self):
        task = Task.objects.create(
            title="Preparar presentación",
            description="Crear las diapositivas para la reunión.",
        )

        response = self.client.patch(
            f"/api/tasks/{task.id}/",
            {"status": "completed"},
            format="json",
        )

        self.assertEqual(response.status_code, 200)
        task.refresh_from_db()
        self.assertEqual(task.status, Task.Status.COMPLETED)

    @override_settings(AI_FAKE_MODE=True)
    def test_analyze_marks_task_as_urgent(self):
        task = Task.objects.create(
            title="Enviar propuesta hoy",
            description="La propuesta debe enviarse antes de las 18 horas.",
        )

        response = self.client.post(f"/api/tasks/{task.id}/analyze/")

        self.assertEqual(response.status_code, 200)
        task.refresh_from_db()
        self.assertEqual(task.category, Task.Category.URGENT)

    @override_settings(AI_FAKE_MODE=True)
    def test_analyze_marks_task_as_not_urgent(self):
        task = Task.objects.create(
            title="Ordenar documentos",
            description="Organizar las carpetas del archivo personal.",
        )

        response = self.client.post(f"/api/tasks/{task.id}/analyze/")

        self.assertEqual(response.status_code, 200)
        task.refresh_from_db()
        self.assertEqual(task.category, Task.Category.NOT_URGENT)
