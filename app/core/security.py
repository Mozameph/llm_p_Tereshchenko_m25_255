from datetime import UTC, datetime, timedelta
from typing import Any

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import settings

_pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Возвращает bcrypt-хеш пароля."""
    return _pwd_context.hash(password)


def verify_password(plain_password: str, password_hash: str) -> bool:
    """Проверяет, соответствует ли пароль сохранённому хешу."""
    return _pwd_context.verify(plain_password, password_hash)


def create_access_token(
    subject: str | int,
    role: str = "user",
    expires_minutes: int | None = None,
) -> str:
    """Создаёт JWT access token с payload: sub, role, iat, exp."""
    now = datetime.now(tz=UTC)
    expire = now + timedelta(
        minutes=expires_minutes if expires_minutes is not None else settings.access_token_expire_minutes
    )
    payload: dict[str, Any] = {
        "sub": str(subject),
        "role": role,
        "iat": int(now.timestamp()),
        "exp": int(expire.timestamp()),
    }
    return jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_alg)


def decode_access_token(token: str) -> dict[str, Any]:
    """Декодирует и валидирует JWT access token, возвращает payload.

    Выбрасывает JWTError, если токен некорректен или просрочен.
    """
    try:
        payload = jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_alg])
    except JWTError as exc:
        raise exc
    return payload
