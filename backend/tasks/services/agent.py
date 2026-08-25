from typing import Literal

from django.conf import settings
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field


class AgentConfigurationError(RuntimeError):
    pass


class TaskAnalysis(BaseModel):
    category: Literal["personal", "work", "urgent", "other"] = Field(
        description="La categoría que mejor representa la tarea."
    )
    subtasks: list[str] = Field(
        min_length=2,
        max_length=5,
        description="Entre 2 y 5 pasos breves y accionables en español.",
    )


class TaskAgent:
    def __init__(self, agent=None):
        self._agent = agent

    def _build_agent(self):
        if not settings.OPENAI_API_KEY:
            raise AgentConfigurationError(
                "Falta OPENAI_API_KEY. Agrégala en el archivo .env."
            )

        model = ChatOpenAI(
            model=settings.OPENAI_MODEL,
            api_key=settings.OPENAI_API_KEY,
        )
        return create_agent(
            model=model,
            tools=[],
            system_prompt=(
                "Eres un agente que organiza tareas. Clasifica cada tarea como "
                "personal, work, urgent u other y propone entre 2 y 5 subtareas "
                "breves, concretas, no repetidas y escritas en español."
            ),
            response_format=TaskAnalysis,
        )

    def analyze(self, title: str, description: str) -> TaskAnalysis:
        if not title.strip() or not description.strip():
            raise ValueError("El título y la descripción son obligatorios.")

        if settings.AI_FAKE_MODE:
            return TaskAnalysis(
                category="work",
                subtasks=[
                    "Revisar el objetivo de la tarea",
                    "Ejecutar los pasos principales",
                    "Comprobar el resultado",
                ],
            )

        agent = self._agent or self._build_agent()
        result = agent.invoke(
            {
                "messages": [
                    {
                        "role": "user",
                        "content": f"Título: {title}\nDescripción: {description}",
                    }
                ]
            }
        )
        return TaskAnalysis.model_validate(result["structured_response"])


def analyze_task(title: str, description: str) -> TaskAnalysis:
    return TaskAgent().analyze(title, description)

