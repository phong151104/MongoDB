from app.models.base_model import BaseModel
from datetime import datetime

class UserModel(BaseModel):
    def __init__(self):
        super().__init__()
        self.collection = self.get_collection('users')
        
    def create_user(self, user_data):
        user_data['created_at'] = datetime.utcnow()
        result = self.collection.insert_one(user_data)
        return str(result.inserted_id)
        
    def get_user(self, user_id):
        return self.collection.find_one({'_id': user_id})
        
    def get_all_users(self):
        return list(self.collection.find())
        
    def update_user(self, user_id, user_data):
        user_data['updated_at'] = datetime.utcnow()
        return self.collection.update_one(
            {'_id': user_id},
            {'$set': user_data}
        )
        
    def delete_user(self, user_id):
        return self.collection.delete_one({'_id': user_id}) 