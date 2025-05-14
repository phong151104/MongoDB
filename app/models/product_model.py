from app.models.base_model import BaseModel
from datetime import datetime
from app.utils.crawler import get_html_from_url
import urllib3
from pymongo import MongoClient
from bson import ObjectId
from app.config.config import Config
from urllib.parse import urlparse

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class ProductModel(BaseModel):
    def __init__(self):
        super().__init__()
        self.collection = self.get_collection('products')
        self.client = MongoClient(Config.MONGODB_URI)
        # Lấy tên database từ URI
        db_name = urlparse(Config.MONGODB_URI).path[1:]  # Bỏ dấu / ở đầu
        self.db = self.client[db_name]
        self.check_results = self.db['html_check_results']  # Collection để lưu kết quả kiểm tra
        
    def create_product(self, product_data):
        link = ""
        if 'link' in product_data and isinstance(product_data['link'], list) and len(product_data['link']) > 0:
            link = product_data['link'][0]
        if link:
            html = get_html_from_url(link)
            product_data['html'] = html if html else ""
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
                product['html'] = html if html else ""
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
            product_data['html'] = html if html else ""
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

    def check_and_store_html_changes(self):
        """
        Kiểm tra HTML của tất cả sản phẩm và lưu kết quả
        Chỉ so sánh html_length, cho phép lệch 1 ký tự thì vẫn coi là giống nhau.
        """
        try:
            products = self.get_all_products()
            mismatched_products = []
            total_checked = 0
            self.check_results.delete_many({})
            for product in products:
                if not product.get('link'):
                    continue
                try:
                    total_checked += 1
                    new_html = get_html_from_url(product['link'])
                    new_html_length = len(new_html) if new_html else 0
                    stored_html_length = product.get('html_length', 0)
                    # So sánh chỉ theo độ dài, cho phép lệch 1 ký tự
                    if abs(new_html_length - stored_html_length) > 1:
                        check_result = {
                            'product_id': str(product['_id']),
                            'product_name': product.get('name', ''),
                            'product_link': product['link'],
                            'stored_html_length': stored_html_length,
                            'new_html_length': new_html_length,
                            'difference': abs(stored_html_length - new_html_length),
                            'stored_html_preview': (product.get('html', '')[:200] + '...') if product.get('html') else None,
                            'new_html_preview': (new_html[:200] + '...') if new_html else None,
                            'checked_at': datetime.utcnow()
                        }
                        self.check_results.insert_one(check_result)
                        mismatched_products.append({
                            'product_id': str(product['_id']),
                            'name': product.get('name', ''),
                            'link': product['link'],
                            'stored_html_length': stored_html_length,
                            'new_html_length': new_html_length,
                            'difference': abs(stored_html_length - new_html_length)
                        })
                except Exception as e:
                    print(f"Lỗi khi kiểm tra sản phẩm {product.get('name')}: {str(e)}")
                    continue
            return {
                'status': 'success',
                'summary': {
                    'total_checked': total_checked,
                    'total_mismatched': len(mismatched_products),
                    'mismatch_percentage': round((len(mismatched_products) / total_checked * 100), 2) if total_checked > 0 else 0,
                    'checked_at': datetime.utcnow()
                },
                'data': mismatched_products
            }
        except Exception as e:
            return {
                'status': 'error',
                'message': str(e)
            }
            
    def get_latest_check_results(self):
        """
        Lấy kết quả kiểm tra HTML gần nhất
        """
        try:
            # Lấy thời gian kiểm tra gần nhất
            latest_check = self.check_results.find_one(
                sort=[('checked_at', -1)]
            )
            
            if not latest_check:
                return {
                    'status': 'success',
                    'message': 'Chưa có kết quả kiểm tra nào',
                    'data': []
                }
                
            # Lấy tất cả kết quả của lần kiểm tra đó
            check_time = latest_check['checked_at']
            results = list(self.check_results.find(
                {'checked_at': check_time}
            ))
            
            # Chuyển ObjectId thành string
            for result in results:
                result['_id'] = str(result['_id'])
            
            return {
                'status': 'success',
                'summary': {
                    'checked_at': check_time,
                    'total_mismatched': len(results)
                },
                'data': results
            }
                
        except Exception as e:
            return {
                'status': 'error',
                'message': str(e)
            } 