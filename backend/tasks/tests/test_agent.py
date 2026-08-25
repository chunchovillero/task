from unittest.mock import Mock

import pytest

from tasks.services.agent import TaskAgent, TaskAnalysis


@pytest.mark.django_db
def test_agent_returns_valid_structured_analysis(settings):
    settings.AI_FAKE_MODE = False
    fake_langchain_agent = Mock()
    fake_langchain_agent.invoke.return_value = {
        "structured_response": TaskAnalysis(
            category="urgent",
            subtasks=["Llamar al cliente", "Enviar la propuesta"],
        )
    }

    result = TaskAgent(agent=fake_langchain_agent).analyze(
        "Enviar propuesta hoy",
        "Preparar y enviar la propuesta antes de las 18:00.",
    )

    assert result.category == "urgent"
    assert result.subtasks == ["Llamar al cliente", "Enviar la propuesta"]
    fake_langchain_agent.invoke.assert_called_once()

