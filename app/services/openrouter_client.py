from typing import Any

import httpx

from app.core.config import settings
from app.core.errors import ExternalServiceError


class OpenRouterClient:
    """Асинхронный клиент для OpenRouter Chat Completions API."""

    def __init__(
        self,
        api_key: str | None = None,
        base_url: str | None = None,
        model: str | None = None,
        site_url: str | None = None,
        app_name: str | None = None,
        timeout: float = 60.0,
    ) -> None:
        self._api_key = api_key or settings.openrouter_api_key
        self._base_url = (base_url or settings.openrouter_base_url).rstrip("/")
        self._model = model or settings.openrouter_model
        self._site_url = site_url or settings.openrouter_site_url
        self._app_name = app_name or settings.openrouter_app_name
        self._timeout = timeout

    def _headers(self) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {self._api_key}",
            "HTTP-Referer": self._site_url,
            "X-Title": self._app_name,
            "Content-Type": "application/json",
        }

    async def chat_completion(
        self,
        messages: list[dict[str, str]],
        temperature: float = 0.7,
        model: str | None = None,
    ) -> str:
        """Выполняет запрос POST /chat/completions и возвращает текст ответа модели."""
        if not self._api_key:
            raise ExternalServiceError(
                "OpenRouter API key is not configured. Set OPENROUTER_API_KEY in .env"
            )

        url = f"{self._base_url}/chat/completions"
        payload: dict[str, Any] = {
            "model": model or self._model,
            "messages": messages,
            "temperature": temperature,
        }

        try:
            async with httpx.AsyncClient(timeout=self._timeout) as client:
                response = await client.post(url, headers=self._headers(), json=payload)
        except httpx.HTTPError as exc:
            raise ExternalServiceError(f"OpenRouter request failed: {exc}") from exc

        if response.status_code >= 400:
            detail = response.text
            raise ExternalServiceError(
                f"OpenRouter returned HTTP {response.status_code}: {detail}"
            )

        try:
            data = response.json()
        except ValueError as exc:
            raise ExternalServiceError("OpenRouter returned non-JSON response") from exc

        try:
            return data["choices"][0]["message"]["content"]
        except (KeyError, IndexError, TypeError) as exc:
            raise ExternalServiceError(
                f"Unexpected OpenRouter response structure: {data}"
            ) from exc
