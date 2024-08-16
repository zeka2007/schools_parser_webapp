__all__ = ['database']

from sqlalchemy import URL

from flask_sqlalchemy import SQLAlchemy

import config


db_url = URL.create(
        "postgresql",
        username=config.postgres_username,
        password=config.postgres_password,
        host=config.postgres_host,
        port=config.postgres_port,
        database=config.postgres_db_name
    )

database = SQLAlchemy()
