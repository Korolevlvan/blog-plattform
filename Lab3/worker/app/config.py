from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    main_database_url: str
    users_database_url: str
    redis_url: str
    push_url: str


settings = Settings()
