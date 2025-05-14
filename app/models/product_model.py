from app.models.base_model import BaseModel
from datetime import datetime

class ProductModel(BaseModel):
    def __init__(self):
        super().__init__()
        self.collection = self.get_collection('products')
        
    def create_product(self, product_data):
        product_data['created_at'] = datetime.utcnow()
        result = self.collection.insert_one(product_data)
        return str(result.inserted_id)
        
    def create_many_products(self, products_data):
        for product in products_data:
            product['created_at'] = datetime.utcnow()
        result = self.collection.insert_many(products_data)
        return [str(id) for id in result.inserted_ids]
        
    def get_product(self, product_id):
        return self.collection.find_one({'_id': product_id})
        
    def get_all_products(self):
        return list(self.collection.find())
        
    def update_product(self, product_id, product_data):
        product_data['updated_at'] = datetime.utcnow()
        return self.collection.update_one(
            {'_id': product_id},
            {'$set': product_data}
        )
        
    def delete_product(self, product_id):
        return self.collection.delete_one({'_id': product_id}) 