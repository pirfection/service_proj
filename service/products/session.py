from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import os
from sqlalchemy import MetaData

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "service.settings")
django.setup()


DATABASE_URL = "postgresql://postgres:postgres@db:5432/postgres"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
metadata = MetaData()
metadata.reflect(bind=engine)

Base = declarative_base(metadata=metadata)


def get_db():
    db = SessionLocal()
    try:
        return db
    finally:
        db.close()


class User(Base):
    __table__ = metadata.tables["subscriptions_user"]
