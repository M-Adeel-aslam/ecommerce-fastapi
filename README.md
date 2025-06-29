# 🛒 Ecommerce Backend API - FastAPI

A fully functional backend for an ecommerce system built using **FastAPI**, **PostgreSQL**, and **SQLAlchemy ORM**. This backend allows customers to register, log in, browse products by category, and place orders, while admins can manage products and categories.

---

## 🚀 Features

- ✅ **User Authentication** (JWT-based)
- ✅ **Product & Category Management** (CRUD)
- ✅ **Order Management** (with multiple items)
- ✅ **Secure Password Hashing**
- ✅ **Relational DB Modeling** using SQLAlchemy
- ✅ **Live API Docs** via FastAPI's OpenAPI UI

---

## 🧩 Tech Stack

- **FastAPI** (Python 3.9+)
- **PostgreSQL**
- **SQLAlchemy**
- **Pydantic**
- **Passlib** (for password hashing)
- **PyJWT**
- **Uvicorn** (ASGI Server)

---

## 📂 Project Structure

```
ecommerce/
│
├── app/
│   ├── models/           # SQLAlchemy models
│   ├── routes/           # All endpoints
│   ├── schemas/          # Pydantic schemas
│   ├── database.py       # DB connection
│   ├── auth.py           # JWT auth functions
│   └── main.py           # Entry point
│
├── .env                  # Environment variables
├── requirements.txt      # Dependencies
├── .gitignore
└── README.md
```

---

## 🔐 Authentication Endpoints

| Method | Endpoint       | Description         |
|--------|----------------|---------------------|
| POST   | /register      | Register a new user |
| POST   | /login         | Login & receive JWT |

---

## 🧾 Product Endpoints (Protected)

| Method | Endpoint          | Description                           |
|--------|-------------------|---------------------------------------|
| POST   | /products         | Create product                        |
| GET    | /products         | Get all products (filter by category) |
| GET    | /products/{id}    | Get product by ID                     |
| PUT    | /products/{id}    | Update product                        |
| DELETE | /products/{id}    | Delete product                        |

---

## 🗂 Category Endpoints (Protected)

| Method | Endpoint             | Description                 |
|--------|----------------------|-----------------------------|
| POST   | /categories          | Create category             |
| GET    | /categories          | Get all categories          |
| GET    | /categories/{id}     | Get category + its products |
| PUT    | /categories/{id}     | Update category             |
| DELETE | /categories/{id}     | Delete category             |

---

## 📦 Order Endpoints (Protected)

| Method | Endpoint           | Description              |
|--------|--------------------|--------------------------|
| POST   | /orders            | Place new order          |
| GET    | /orders            | List user's orders       |
| GET    | /orders/{id}       | View order detail        |
| PUT    | /orders/{id}       | Update order (status)    |
| DELETE | /orders/{id}       | Cancel/delete order      |

---

## 🧠 Optional AI & Aggregation

| Method | Endpoint                      | Description         |
|--------|-------------------------------|---------------------|
| GET    | /orders/{id}/summary          | Summarized order    |
| GET    | /products/recommendations     | Product suggestions |

---

## ⚙️ Setup Instructions

1. **Clone the repository**
```bash
git clone https://github.com/YOUR_USERNAME/ecommerce.git
cd ecommerce
```

2. **Create & activate virtual environment**
```bash
python -m venv venv
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure `.env`**
```env
DATABASE_URL=postgresql://user:password@localhost/dbname
KEY=your_jwt_secret_key
ALGORITHM=HS256
EXPIRE_TOKEN_TIME=30
```

5. **Run the app**
```bash
uvicorn app.main:app --reload
```

6. **Visit Docs**
```
http://127.0.0.1:8000/docs
```
---

## 📝 License

This project is for educational purposes. Feel free to extend or deploy it as needed.

---
