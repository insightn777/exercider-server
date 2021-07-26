from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from configs import get_settings

db = create_engine(get_settings().SQLALCHEMY_DATABASE_URI)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=db)


def get_db():
    _db = SessionLocal()
    try:
        yield _db
    finally:
        _db.close()
