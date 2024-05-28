__all__ = ['BaseModel', 'Student', 'Message',
           'session_maker', 'create_database', 'async_engine']

from sqlalchemy import URL

from flask_sqlalchemy import SQLAlchemy

import config
from .base import BaseModel
from .student import Student
from .messages import Message

db_url = URL.create(
        "postgresql",
        username=config.postgres_username,
        password=config.postgres_password,
        host=config.postgres_host,
        port=config.postgres_port,
        database=config.postgres_db_name
    )

database = SQLAlchemy()