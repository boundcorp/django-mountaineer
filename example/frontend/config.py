from mountaineer import ConfigBase
from pydantic_settings import SettingsConfigDict


class AppConfig(ConfigBase):
    PACKAGE: str | None = "frontend"
    find_controllers: list[str] = []

    model_config = SettingsConfigDict(env_file=(".env",))
