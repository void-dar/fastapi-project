from pydantic_settings import BaseSettings, SettingsConfigDict
import os
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    DATABASE_URL: str #= os.getenv("DATABASE_URL")
    JWT_SECRET: str
    JWT_ALGORITM: str

    
    model_config = SettingsConfigDict(env_file = ".env")

settings = Settings()
