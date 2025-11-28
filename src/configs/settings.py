from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')

    database_url: str
    environment: str = "production"
    title: str = "API"
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int


settings = Settings()
