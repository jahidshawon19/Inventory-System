# 📦 Arfaana Inventory Management System

A simple and modern **Inventory Management System** built with **Django**.  
This project helps track products, manage stock, handle issuing/returning items, and generate sales reports.

---
# Live
inventory-system-lb7w.onrender.com
username: admin
password: admin

## 🚀 Features

### 📦 Product Management
- Add, update, delete products
- Auto calculation of total price
- Stock quantity tracking

### 🔄 Stock Operations
- Issue products (reduce stock)
- Return products (increase stock)
- Prevent issuing more than available stock

### 📊 Reports & Analytics
- Daily Issue Report
- Daily Sales Report
- Monthly Sales Report (with filter)
- Total sales & quantity tracking

### ⚠️ Alerts
- Low stock alert system

### 🔐 Authentication
- Login / Logout system
- Protected routes for authorized users

### 📥 Export
- Download reports in CSV (Excel supported)

---

## 🖥️ Tech Stack

- **Backend:** Django (Python)
- **Frontend:** HTML, Bootstrap 5
- **Database:** SQLite (default)
- **Others:** Django ORM, Template Engine

---

## 📁 Project Structure

inventory/
│
├── inventory/ # Main project settings
├── products/ # Main app
│ ├── models.py
│ ├── views.py
│ ├── urls.py
│ ├── templates/
│ └── forms.py
│
├── db.sqlite3
└── manage.py


---

## ⚙️ Installation

### 1️⃣ Clone Repository
```bash
git clone https://github.com/your-username/inventory-system.git
cd inventory-system

python -m venv venv
venv\Scripts\activate   # Windows
