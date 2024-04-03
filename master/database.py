from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from settings import settings


DATABASE_URL = f"postgresql+psycopg2://{settings.user}:{settings.password}@{settings.host}:{settings.port}/{settings.db_name}"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autoflush=False, bind=engine)

Base = declarative_base()


