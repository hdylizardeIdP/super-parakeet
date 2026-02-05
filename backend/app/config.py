from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "postgresql://realestate:realestate@localhost:5432/realestate"

    class Config:
        env_file = ".env"


settings = Settings()
