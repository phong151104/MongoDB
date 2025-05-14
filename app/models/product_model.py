from app.models.base_model import BaseModel
from datetime import datetime
from app.utils.crawler import get_html_from_url
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class ProductModel(BaseModel):
    def __init__(self):
        super().__init__()
        self.collection = self.get_collection('products')
        
    def create_product(self, product_data):
        link = ""
        if 'link' in product_data and isinstance(product_data['link'], list) and len(product_data['link']) > 0:
            link = product_data['link'][0]
        if link:
            html = get_html_from_url(link)
            product_data['html'] = html[:300] if html else ""
            product_data['html_length'] = len(html) if html else 0
        else:
            product_data['html'] = ""
            product_data['html_length'] = 0
        product_data['created_at'] = datetime.utcnow()
        result = self.collection.insert_one(product_data)
        return str(result.inserted_id)
        
    def create_many_products(self, products_data):
        for product in products_data:
            link = ""
            if 'link' in product and isinstance(product['link'], list) and len(product['link']) > 0:
                link = product['link'][0]
            if link:
                html = get_html_from_url(link)
                product['html'] = html[:300] if html else ""
                product['html_length'] = len(html) if html else 0
            else:
                product['html'] = ""
                product['html_length'] = 0
            product['created_at'] = datetime.utcnow()
        result = self.collection.insert_many(products_data)
        return [str(id) for id in result.inserted_ids]
        
    def get_product(self, product_id):
        return self.collection.find_one({'_id': product_id})
        
    def get_all_products(self):
        return list(self.collection.find())
        
    def update_product(self, product_id, product_data):
        link = ""
        if 'link' in product_data and isinstance(product_data['link'], list) and len(product_data['link']) > 0:
            link = product_data['link'][0]
        if link:
            html = get_html_from_url(link)
            product_data['html'] = html[:300] if html else ""
            product_data['html_length'] = len(html) if html else 0
        else:
            product_data['html'] = ""
            product_data['html_length'] = 0
        product_data['updated_at'] = datetime.utcnow()
        return self.collection.update_one(
            {'_id': product_id},
            {'$set': product_data}
        )
        
    def delete_product(self, product_id):
        return self.collection.delete_one({'_id': product_id})
        
    def update_all_products_html(self):
        products = self.collection.find({})
        updated_count = 0
        total = self.collection.count_documents({})
        print(f"Total products to update: {total}")
        for idx, product in enumerate(products, 1):
            link = ""
            if isinstance(product.get('link', ""), list) and len(product['link']) > 0:
                link = product['link'][0]
            elif isinstance(product.get('link', ""), str):
                link = product['link']
            print(f"[{idx}/{total}] Crawling: {link}")
            if link:
                html = get_html_from_url(link)
                html_content = html if html else ""
                html_length = len(html) if html else 0
            else:
                html_content = ""
                html_length = 0
            result = self.collection.update_one(
                {'_id': product['_id']},
                {'$set': {'html': html_content, 'html_length': html_length, 'updated_at': datetime.utcnow()}}
            )
            if result.modified_count > 0:
                updated_count += 1
            print(f"    Done. HTML length: {html_length}")
        print(f"Updated {updated_count} products.")
        return updated_count 