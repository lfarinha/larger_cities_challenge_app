import os

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    General Settings for the Application
    """

    # app config
    app_name: str = "Suggestions API Challenge"
    host: str = "0.0.0.0"
    port: int = 5000

    # project root

