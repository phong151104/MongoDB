from flask import Blueprint, request, jsonify
from app.controllers.product_controller import ProductController

product_bp = Blueprint('product', __name__)
product_controller = ProductController()

@product_bp.route('/products', methods=['POST'])
def create_product():
    product_data = request.get_json()
    result = product_controller.create_product(product_data)
    return jsonify(result), 201 if result['status'] == 'success' else 400

@product_bp.route('/products/bulk', methods=['POST'])
def create_many_products():
    products_data = request.get_json()
    result = product_controller.create_many_products(products_data)
    return jsonify(result), 201 if result['status'] == 'success' else 400

@product_bp.route('/products/<product_id>', methods=['GET'])
def get_product(product_id):
    result = product_controller.get_product(product_id)
    return jsonify(result), 200 if result['status'] == 'success' else 404

@product_bp.route('/products', methods=['GET'])
def get_all_products():
    result = product_controller.get_all_products()
    return jsonify(result), 200 if result['status'] == 'success' else 400

@product_bp.route('/products/<product_id>', methods=['PUT'])
def update_product(product_id):
    product_data = request.get_json()
    result = product_controller.update_product(product_id, product_data)
    return jsonify(result), 200 if result['status'] == 'success' else 404

@product_bp.route('/products/<product_id>', methods=['DELETE'])
def delete_product(product_id):
    result = product_controller.delete_product(product_id)
    return jsonify(result), 200 if result['status'] == 'success' else 404

@product_bp.route('/products/update-html', methods=['POST'])
def update_all_products_html():
    result = product_controller.update_all_products_html()
    return jsonify(result), 200 if result['status'] == 'success' else 400

@product_bp.route('/check-and-store-html', methods=['GET'])
def check_and_store_html():
    result = product_controller.check_and_store_html_changes()
    return jsonify(result), 200 if result['status'] == 'success' else 500

@product_bp.route('/latest-html-check-results', methods=['GET'])
def get_latest_check_results():
    result = product_controller.get_latest_check_results()
    return jsonify(result), 200 if result['status'] == 'success' else 500 