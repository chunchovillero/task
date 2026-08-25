import pytest
from rest_framework.test import APIClient

from tasks.models import Task
from tasks.services.agent import TaskAnalysis


@pytest.fixture
def api_client():
    return APIClient()


@pytest.mark.django_db
def test_create_list_and_complete_task(api_client):
    create_response = api_client.post(
        "/api/tasks/",
        {
            "title": "Preparar entrevista",
            "description": "Repasar Django y Docker para la prueba.",
        },
        format="json",
    )

    assert create_response.status_code == 201
    task_id = create_response.data["id"]

    list_response = api_client.get("/api/tasks/")
    assert list_response.status_code == 200
    assert len(list_response.data) == 1

    update_response = api_client.patch(
        f"/api/tasks/{task_id}/",
        {"status": "completed"},
        format="json",
    )
    assert update_response.status_code == 200
    assert update_response.data["status"] == "completed"


@pytest.mark.django_db
def test_analyze_endpoint_persists_agent_result(api_client, monkeypatch):
    task = Task.objects.create(
        title="Preparar informe",
        description="Enviar el informe de avance al cliente hoy.",
    )
    monkeypatch.setattr(
        "tasks.views.analyze_task",
        lambda title, description: TaskAnalysis(
            category="urgent",
            subtasks=["Revisar métricas", "Redactar informe", "Enviar al cliente"],
        ),
    )

    response = api_client.post(f"/api/tasks/{task.id}/analyze/")

    assert response.status_code == 200
    task.refresh_from_db()
    assert task.category == "urgent"
    assert len(task.subtasks) == 3

