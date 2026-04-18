from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Настройки приложения, читаемые из переменных окружения .env."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Общие
    app_name: str = "llm-p"
    env: str = "local"

    # JWT
    jwt_secret: str = "change_me_super_secret"
    jwt_alg: str = "HS256"
    access_token_expire_minutes: int = 60

    # SQLite
    sqlite_path: str = "./app.db"

    # OpenRouter
    openrouter_api_key: str = ""
    openrouter_base_url: str = "https://openrouter.ai/api/v1"
    openrouter_model: str = "stepfun/step-3.5-flash:free"
    openrouter_site_url: str = "https://example.com"
    openrouter_app_name: str = "llm-fastapi-openrouter"


settings = Settings()
