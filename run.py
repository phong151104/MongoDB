from flask import Flask
from flask_cors import CORS
from app.views.user_view import user_bp
from app.views.product_view import product_bp
from app.config.config import Config
from mongoengine import connect

app = Flask(__name__)
CORS(app)

# Kết nối MongoDB
connect(host=Config.MONGODB_URI)

# Đăng ký blueprints
app.register_blueprint(user_bp, url_prefix='/api')
app.register_blueprint(product_bp, url_prefix='/api')

if __name__ == '__main__':
    app.run(debug=Config.DEBUG) 