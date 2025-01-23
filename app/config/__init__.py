from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    mongo_uri: str
    rabbitmq_uri: str
    github_token: str
    github_organization_name: str

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()