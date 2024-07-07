import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg2://apphk:testuser@localhost/app")
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost/0")
SECRET_KEY = os.getenv("SECRET_KEY", "RxVnh4orHdFSUFTLgMvuan6K2Xlf8YC83fxwgaaBlmY")
