class AppError(Exception):
    """Базовое исключение приложения."""

    def __init__(self, message: str = "Application error") -> None:
        super().__init__(message)
        self.message = message


class ConflictError(AppError):
    """Конфликт данных (например, email уже существует)."""


class UnauthorizedError(AppError):
    """Неавторизован (неверные учётные данные или невалидный токен)."""


class ForbiddenError(AppError):
    """Запрещено (недостаточно прав)."""


class NotFoundError(AppError):
    """Объект не найден."""


class ExternalServiceError(AppError):
    """Ошибка внешнего сервиса."""
