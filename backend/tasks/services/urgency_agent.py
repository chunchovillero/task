from django.conf import settings
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field


class AgentConfigurationError(RuntimeError):
    pass


class UrgencyAnalysis(BaseModel):
    urgent: bool = Field(
        description="Indica si la tarea requiere atención prioritaria por tiempo o impacto."
    )


class UrgencyAgent:
    def __init__(self, agent=None):
        self._agent = agent

    def _build_agent(self):
        if not settings.OPENAI_API_KEY:
            raise AgentConfigurationError("Falta configurar OPENAI_API_KEY.")

        model = ChatOpenAI(
            model=settings.OPENAI_MODEL,
            api_key=settings.OPENAI_API_KEY,
        )
        return create_agent(
            model=model,
            tools=[],
            system_prompt=(
                "Clasifica tareas en urgente o no urgente. Una tarea es urgente cuando "
                "tiene un plazo cercano explícito, bloquea trabajo importante o implica "
                "un impacto grave si se retrasa. Devuelve solo la salida estructurada."
            ),
            response_format=UrgencyAnalysis,
        )

    def analyze(self, title: str, description: str) -> UrgencyAnalysis:
        if settings.AI_FAKE_MODE:
            text = f"{title} {description}".lower()
            urgent_words = (
                "urgente",
                "hoy",
                "mañana",
                "inmediato",
                "vencimiento",
                "urgent",
                "today",
                "tomorrow",
                "immediate",
                "deadline",
            )
            return UrgencyAnalysis(urgent=any(word in text for word in urgent_words))

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
        return UrgencyAnalysis.model_validate(result["structured_response"])


def analyze_urgency(title: str, description: str) -> UrgencyAnalysis:
    return UrgencyAgent().analyze(title, description)
