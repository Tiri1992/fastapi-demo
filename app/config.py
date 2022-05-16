"""Performs data validation and checks on env variables."""
from pydantic import BaseSettings


class Settings(BaseSettings):
    """Performs validation on env variables.
    I.e. it checks that all these env variables have been set on host.
    """
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    class Config:
        """Tells pydantic to look for env variables in this file."""
        env_file = ".env"


# Stores all env variables as attributes of this instance
settings = Settings()
