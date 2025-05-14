# Flask MongoDB MVC API

Đây là một ứng dụng API được xây dựng với Flask và MongoDB theo mô hình MVC.

## Cài đặt

1. Tạo môi trường ảo:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

2. Cài đặt dependencies:
```bash
pip install -r requirements.txt
```

3. Tạo file .env và cấu hình:
```
MONGODB_URI=mongodb://localhost:27017
DB_NAME=your_database_name
```

4. Chạy ứng dụng:
```bash
python run.py
```

## Cấu trúc thư mục

```
├── app/
│   ├── models/         # Định nghĩa models và tương tác với MongoDB
│   ├── views/          # Xử lý template và response
│   ├── controllers/    # Xử lý logic nghiệp vụ
│   ├── config/         # Cấu hình ứng dụng
│   └── utils/          # Tiện ích
├── requirements.txt    # Dependencies
└── run.py             # File chạy ứng dụng
``` 