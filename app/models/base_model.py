from pymongo import MongoClient
from app.config.config import Config

class BaseModel:
    def __init__(self):
        self.client = MongoClient(Config.MONGODB_URI)
        self.db = self.client[Config.DB_NAME]
        
    def get_collection(self, collection_name):
        return self.db[collection_name]
        
    def close(self):
        self.client.close() 