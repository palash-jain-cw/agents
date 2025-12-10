from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv
import os
import logging
from pathlib import Path
from typing import Optional

# Import logging config module to ensure logging is configured on import
import agents.core.logging_config  # noqa: F401

load_dotenv()

project_root_dir = Path(__file__).parent.parent.parent

logger = logging.getLogger(__name__)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=os.path.join(project_root_dir, ".env"), env_file_encoding="utf-8"
    )
    AWS_ACCESS_KEY_ID: Optional[str] = None
    AWS_SECRET_ACCESS_KEY: Optional[str] = None
    AWS_DEFAULT_REGION: Optional[str] = None


settings = Settings()
