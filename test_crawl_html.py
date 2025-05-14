from app.models.product_model import ProductModel
from bson import ObjectId

if __name__ == "__main__":
    model = ProductModel()
    # Lấy 5 sản phẩm đầu tiên có link hợp lệ
    products = model.collection.find({
        'link': {'$exists': True, '$ne': ""}
    }).limit(5)
    total = 5
    for product in products:
        link = ""
        if isinstance(product.get('link', ""), list) and len(product['link']) > 0:
            link = product['link'][0]
        elif isinstance(product.get('link', ""), str):
            link = product['link']
        print(f"\nProduct _id: {product['_id']}")
        print(f"Link: {link}")
        if link:
            html = model.collection.find_one({'_id': product['_id']}).get('html', None)
            if html:
                print(f"HTML length: {len(html)}")
                print(f"HTML preview: {html[:300]}...")
            else:
                print("No HTML crawled yet.")
        else:
            print("No link available.") 