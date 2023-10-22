from typing import Optional

from pydantic.env_settings import BaseSettings
from pydantic.fields import Field


class Settings(BaseSettings):

    API_KEY_NAME : Optional[str] = Field(None, env="API_KEY_NAME")
    ZAMA_CHALLENGE_API_KEY : Optional[str] = Field(None, env="ZAMA_CHALLENGE_API_KEY")


settings = Settings()