from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import ChatMessage


class ChatMessagesRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def add(self, user_id: int, role: str, content: str) -> ChatMessage:
        message = ChatMessage(user_id=user_id, role=role, content=content)
        self._session.add(message)
        await self._session.commit()
        await self._session.refresh(message)
        return message

    async def get_last_n(self, user_id: int, limit: int) -> list[ChatMessage]:
        """Возвращает последние N сообщений пользователя в хронологическом порядке."""
        if limit <= 0:
            return []
        stmt = (
            select(ChatMessage)
            .where(ChatMessage.user_id == user_id)
            .order_by(ChatMessage.id.desc())
            .limit(limit)
        )
        result = await self._session.execute(stmt)
        rows = list(result.scalars().all())
        rows.reverse()
        return rows

    async def list_all(self, user_id: int) -> list[ChatMessage]:
        stmt = (
            select(ChatMessage)
            .where(ChatMessage.user_id == user_id)
            .order_by(ChatMessage.id.asc())
        )
        result = await self._session.execute(stmt)
        return list(result.scalars().all())

    async def clear_for_user(self, user_id: int) -> int:
        stmt = delete(ChatMessage).where(ChatMessage.user_id == user_id)
        result = await self._session.execute(stmt)
        await self._session.commit()
        return result.rowcount or 0
