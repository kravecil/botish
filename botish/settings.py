from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr, Field, MongoDsn, RedisDsn


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    telegram_bot_token: SecretStr = Field(default=...)
    binance_api_token: SecretStr = Field(default=...)
    db_dsn: MongoDsn = Field(default=...)
    db_name: str = Field(default=...)
    redis_dsn: RedisDsn = Field(default=...)


settings = Settings()
