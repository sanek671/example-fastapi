from pydantic_settings import BaseSettings
from pydantic import ConfigDict, field_validator
from typing import Optional


class Settings(BaseSettings):
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: Optional[int]

    @field_validator('access_token_expire_minutes', mode='before')
    def parse_expire_minutes(cls, v):
        if isinstance(v, str) and v.strip() in ['***', '']:
            return 30
        return int(v)

    model_config = ConfigDict(env_file=".env")


settings = Settings()
