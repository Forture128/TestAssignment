from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from application.config import config

engine = create_engine(config.SQLALCHEMY_DB_URI)
SessionLocal = sessionmaker(engine, autoflush=False)

Base = declarative_base()


async def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()
