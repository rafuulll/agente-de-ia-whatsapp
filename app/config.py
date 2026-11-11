from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "agente-de-ia-whatsapp"
    app_env: str = "development"
    meta_verify_token: str

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
