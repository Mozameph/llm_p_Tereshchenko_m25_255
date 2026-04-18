from app.db.models import ChatMessage
from app.repositories.chat_messages import ChatMessagesRepository
from app.services.openrouter_client import OpenRouterClient


class ChatUseCase:
    def __init__(
        self,
        messages_repo: ChatMessagesRepository,
        openrouter: OpenRouterClient,
    ) -> None:
        self._messages = messages_repo
        self._openrouter = openrouter

    async def ask(
        self,
        user_id: int,
        prompt: str,
        system: str | None = None,
        max_history: int = 10,
        temperature: float = 0.7,
    ) -> str:
        """Полный цикл общения с LLM: сбор контекста, сохранение запроса,
        вызов OpenRouter, сохранение ответа, возврат текста."""

        # Собираем список messages для модели
        messages: list[dict[str, str]] = []

        # System-инструкция, если есть
        if system:
            messages.append({"role": "system", "content": system})

        # История пользователя из базы
        history = await self._messages.get_last_n(user_id=user_id, limit=max_history)
        for msg in history:
            messages.append({"role": msg.role, "content": msg.content})

        # Текущий prompt
        messages.append({"role": "user", "content": prompt})

        # Сохраняем prompt в БД как сообщение роли user
        await self._messages.add(user_id=user_id, role="user", content=prompt)

        # Вызываем OpenRouter
        answer = await self._openrouter.chat_completion(
            messages=messages,
            temperature=temperature,
        )

        # Сохраняем ответ как сообщение роли assistant
        await self._messages.add(user_id=user_id, role="assistant", content=answer)

        return answer

    async def get_history(self, user_id: int) -> list[ChatMessage]:
        return await self._messages.list_all(user_id=user_id)

    async def clear_history(self, user_id: int) -> int:
        return await self._messages.clear_for_user(user_id=user_id)
