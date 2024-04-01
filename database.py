from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    user: str
    password: str
    host: str
    port: str
    db_name: str

    model_config = SettingsConfigDict(env_file='.env')


def get_settings():
    return Settings()

settings = get_settings()

DATABASE_URL = f"postgresql+psycopg2://{settings.user}:{settings.password}@{settings.host}:{settings.port}/{settings.db_name}"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autoflush=False, bind=engine)

Base = declarative_base()

