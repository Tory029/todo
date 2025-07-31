from dotenv import load_dotenv
import os

load_dotenv()

class Settings():
    DATABASE_URL = os.getenv("DATABASE_URL")
    PORT = os.getenv("PORT")
    HOST = os.getenv("HOST")


settings = Settings()
