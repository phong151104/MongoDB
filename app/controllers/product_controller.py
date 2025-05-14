from app.models.product_model import ProductModel
from bson import ObjectId

class ProductController:
    def __init__(self):
        self.model = ProductModel()
        
    def create_product(self, product_data):
        try:
            product_id = self.model.create_product(product_data)
            return {'status': 'success', 'product_id': product_id}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
            
    def create_many_products(self, products_data):
        try:
            product_ids = self.model.create_many_products(products_data)
            return {'status': 'success', 'product_ids': product_ids}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
            
    def get_product(self, product_id):
        try:
            product = self.model.get_product(ObjectId(product_id))
            if product:
                product['_id'] = str(product['_id'])
                return {'status': 'success', 'product': product}
            return {'status': 'error', 'message': 'Product not found'}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
            
    def get_all_products(self):
        try:
            products = self.model.get_all_products()
            for product in products:
                product['_id'] = str(product['_id'])
            return {'status': 'success', 'products': products}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
            
    def update_product(self, product_id, product_data):
        try:
            result = self.model.update_product(ObjectId(product_id), product_data)
            if result.modified_count > 0:
                return {'status': 'success', 'message': 'Product updated successfully'}
            return {'status': 'error', 'message': 'Product not found'}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
            
    def delete_product(self, product_id):
        try:
            result = self.model.delete_product(ObjectId(product_id))
            if result.deleted_count > 0:
                return {'status': 'success', 'message': 'Product deleted successfully'}
            return {'status': 'error', 'message': 'Product not found'}
        except Exception as e:
            return {'status': 'error', 'message': str(e)} 