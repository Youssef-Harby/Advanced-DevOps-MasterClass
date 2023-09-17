from pydantic import BaseModel, SecretStr, Field
import os
from dotenv import load_dotenv


class DatabaseSettings(BaseModel):
    user: str = Field(..., env="POSTGRES_USER")
    password: SecretStr = Field(..., env="POSTGRES_PASSWORD")
    db: str = Field(..., env="POSTGRES_DB")
    host: str = Field(..., env="POSTGRES_HOST")
    port: str = Field(..., env="POSTGRES_PORT")

    @classmethod
    def from_env(cls):
        try:
            load_dotenv()
        except Exception as e:
            print("Error: Could not load environment variables from .env file")
            pass
        return cls(
            user=os.environ.get("POSTGRES_USER"),
            password=os.environ.get("POSTGRES_PASSWORD"),
            db=os.environ.get("POSTGRES_DB"),
            host=os.environ.get("POSTGRES_HOST"),
            port=os.environ.get("POSTGRES_PORT"),
        )

    def database_url(self):
        return f"postgresql://{self.user}:{self.password.get_secret_value()}@{self.host}:{self.port}/{self.db}"
