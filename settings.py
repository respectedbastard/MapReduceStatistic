from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    user: str
    password: str
    host: str
    port: str
    db_name: str

    cash_capacity: int
    slave_quantity: int

    class Config:
        env_file = '.env'


def get_settings():
    return Settings()

settings = get_settings()
