from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import Config
from models import Base

engine = create_engine(
    f"postgresql://{Config.DB_USER}:{Config.DB_PASSWORD}@{Config.DB_HOST}/{Config.DB_NAME}",
)

Base.metadata.create_all(bind=engine)

# Создаем sessionmaker, привязанный к engine
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)