from __future__ import annotations

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    bot_token: SecretStr = SecretStr("")
    test_chat_id: int = -111

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


config = Settings()
