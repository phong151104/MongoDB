from app.models.user_model import UserModel
from bson import ObjectId

class UserController:
    def __init__(self):
        self.model = UserModel()
        
    def create_user(self, user_data):
        try:
            user_id = self.model.create_user(user_data)
            return {'status': 'success', 'user_id': user_id}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
            
    def get_user(self, user_id):
        try:
            user = self.model.get_user(ObjectId(user_id))
            if user:
                user['_id'] = str(user['_id'])
                return {'status': 'success', 'user': user}
            return {'status': 'error', 'message': 'User not found'}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
            
    def get_all_users(self):
        try:
            users = self.model.get_all_users()
            for user in users:
                user['_id'] = str(user['_id'])
            return {'status': 'success', 'users': users}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
            
    def update_user(self, user_id, user_data):
        try:
            result = self.model.update_user(ObjectId(user_id), user_data)
            if result.modified_count > 0:
                return {'status': 'success', 'message': 'User updated successfully'}
            return {'status': 'error', 'message': 'User not found'}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
            
    def delete_user(self, user_id):
        try:
            result = self.model.delete_user(ObjectId(user_id))
            if result.deleted_count > 0:
                return {'status': 'success', 'message': 'User deleted successfully'}
            return {'status': 'error', 'message': 'User not found'}
        except Exception as e:
            return {'status': 'error', 'message': str(e)} 