from fastapi import Security
from fastapi.security.api_key import APIKeyHeader

from . import config as env
from . import exceptions as custom_exception
from .models import models
from .database.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)
API_KEY = env.settings.API_KEY
api_key_header = APIKeyHeader(name=env.settings.API_KEY_NAME, auto_error=False)


def get_api_key(api_key_header: str = Security(api_key_header)):
    if api_key_header == API_KEY:
        return api_key_header
    else:
        raise custom_exception.ForbiddenException()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()