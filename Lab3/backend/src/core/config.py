from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    main_database_url: str
    redis_url: str
    jwt_secret: str
    jwt_algorithm: str = "HS256"


settings = Settings()
