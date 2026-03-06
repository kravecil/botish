from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr, Field
from dotenv import find_dotenv


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        extra="ignore",
        env_file=find_dotenv(),
        env_file_encoding="utf-8",
    )

    telegram_bot_token: SecretStr = Field(default=...)
    binance_api_token: SecretStr = Field(default=...)

    db_host: str = Field(default=...)
    db_port: str = Field(default=...)
    db_username: str = Field(default=...)
    db_password: str = Field(default=...)
    db_name: str = Field(default=...)


settings = Settings()
