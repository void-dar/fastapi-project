from pydantic_settings import BaseSettings, SettingsConfigDict
import os
from dotenv import load_dotenv #use load_env once env file isn't loading


load_dotenv()

class Settings(BaseSettings):
    DATABASE_URL : str =  os.getenv("DATABASE_URL")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )



Config = Settings()