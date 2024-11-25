import os
from dotenv import load_dotenv

load_dotenv()

DEBUG = os.getenv("DEBUG")
SECRET_KEY = os.getenv("SECRET_KEY")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")
JWT_EXPIRE = int(os.getenv("JWT_EXPIRE"))

DATABASE_URL = os.getenv("DATABASE_URL")
REDIS_URL = os.getenv("REDIS_URL")
