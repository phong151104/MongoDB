import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    DB_NAME = os.getenv('DB_NAME', 'flask_mongodb_mvc')
    MONGODB_URI = os.getenv('MONGODB_URI', f'mongodb://localhost:27017/flask_mongodb_mvc')
    DEBUG = os.getenv('FLASK_DEBUG', 'True').lower() in ('true', '1', 't') 