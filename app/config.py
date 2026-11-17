from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "agente-de-ia-whatsapp"
    app_env: str = "development"
    meta_verify_token: str
    meta_access_token: str = ""
    meta_phone_number_id: str = ""
    meta_graph_version: str = "v23.0"
    gemini_api_key: str
    gemini_model: str = "gemini-3.5-flash-lite"
    salao_nome: str = "Salão Exemplo"
    profissional_nome: str = "Profissional Exemplo"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
