from flask import Blueprint, request, jsonify
from app.controllers.user_controller import UserController

user_bp = Blueprint('user', __name__)
user_controller = UserController()

@user_bp.route('/users', methods=['POST'])
def create_user():
    user_data = request.get_json()
    result = user_controller.create_user(user_data)
    return jsonify(result), 201 if result['status'] == 'success' else 400

@user_bp.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    result = user_controller.get_user(user_id)
    return jsonify(result), 200 if result['status'] == 'success' else 404

@user_bp.route('/users', methods=['GET'])
def get_all_users():
    result = user_controller.get_all_users()
    return jsonify(result), 200 if result['status'] == 'success' else 400

@user_bp.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    user_data = request.get_json()
    result = user_controller.update_user(user_id, user_data)
    return jsonify(result), 200 if result['status'] == 'success' else 404

@user_bp.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    result = user_controller.delete_user(user_id)
    return jsonify(result), 200 if result['status'] == 'success' else 404 