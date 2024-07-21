import os
from dotenv import load_dotenv

load_dotenv()

postgres_username = os.getenv("POSTGRES_USER")
postgres_password = os.getenv("POSTGRES_PASSWORD")
postgres_db_name = os.getenv("POSTGRES_DB")
postgres_port = os.getenv("POSTGRES_PORT")
postgres_host = os.getenv("POSTGRES_HOST")

bot_token = os.getenv("BOT_TOKEN")
host = os.getenv("WEB_HOST")

debug = True
