from datetime import datetime

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    prompt: str = Field(min_length=1, description="Основной текст запроса к модели")
    system: str | None = Field(default=None, description="Необязательная системная инструкция")
    max_history: int = Field(
        default=10,
        ge=0,
        le=100,
        description="Сколько последних сообщений пользователя включать в контекст",
    )
    temperature: float = Field(
        default=0.7,
        ge=0.0,
        le=2.0,
        description="Параметр 'креативности' модели",
    )


class ChatResponse(BaseModel):
    answer: str


class ChatMessagePublic(BaseModel):
    id: int
    role: str
    content: str
    created_at: datetime

    model_config = {"from_attributes": True}
