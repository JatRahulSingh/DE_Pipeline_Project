# 📦 Food Delivery Data Engineering Pipeline  
### **Python → PySpark → MongoDB | End-to-End Batch ETL Project**

This project demonstrates a complete batch **Data Engineering pipeline** that simulates a real-world food delivery platform (similar to Swiggy/Zomato).  
It generates synthetic data using Python, processes and analyzes it using **PySpark**, and stores enriched datasets and aggregated analytics into **MongoDB**.

The entire workflow is structured in a clean, production-style format to showcase real Data Engineering concepts.

---

## 🚀 Project Overview

### **✔ 1. Data Generation (Python)**  
A Python script generates synthetic food-delivery orders with fields like:
- Order details  
- User information  
- Restaurant & cuisine  
- Payment method  
- Delivery ratings  
- Revenue values  

Generated data is saved as a CSV inside `data/raw/`.

---

### **✔ 2. Batch Data Processing (PySpark)**  
PySpark is used to read, clean, transform, and analyze the data.

Key features:
- Schema inference  
- Null/invalid record handling  
- Derived columns:  
  - `avg_order_value_per_item`  
  - `is_high_value_order`  
- Aggregations:  
  - Revenue & order count by city  
  - Restaurant-level metrics  
  - Ratings analysis  

---

### **✔ 3. Storage Layer (MongoDB)**  
Processed datasets are written into **MongoDB** collections:

| Collection            | Description                                 |
|-----------------------|----------------------------------------------|
| `orders_detail`       | Enriched individual orders                   |
| `city_metrics`        | City-level aggregated metrics                |
| `restaurant_metrics`  | Restaurant performance summaries             |

This mirrors real-world analytical storage in NoSQL systems.

---

## 🏗️ Project Architecture

```
        +----------------------+
        |  Python Generator    |
        | (generate_orders.py) |
        +----------+-----------+
                   |
                   v
        +----------------------+
        |   Raw CSV Dataset    |
        |   (data/raw/)        |
        +----------+-----------+
                   |
                   v
        +----------------------+
        |   PySpark ETL Job    |
        | (analyze_orders_     |
        |        _spark.py)    |
        +----------+-----------+
                   |
                   v
        +----------------------+
        |      MongoDB         |
        | orders_detail        |
        | city_metrics         |
        | restaurant_metrics   |
        +----------------------+
```

---

## 📁 Folder Structure

```
DE_Pipeline_Project/
│
├── data/
│   └── raw/
│       └── food_orders.csv
│
├── scripts/
│   ├── generate_orders.py
│   └── analyze_orders_spark.py
│
├── requirements.txt
└── README.md
```

---

## ⚙️ Requirements

**Python**

**Java (for pyspark)**

**Mongodb**

**Pyspark**

Install dependencies:

```
pip install -r requirements.txt
```

Dependencies include:
- pyspark  
- pymongo  

MongoDB must be installed and running:
```
mongod --dbpath mongodb-data
```

---

## ▶️ How to Run the Project

### **1. Generate synthetic orders**
```
python scripts/generate_orders.py
```

---

### **2. Start MongoDB**
```
mongod --dbpath mongodb-data
```

---

### **3. Run PySpark ETL job**
```
spark-submit scripts/analyze_orders_spark.py
```

---

### **4. Verify results in MongoDB**
```
mongosh
use food_delivery
show collections
db.orders_detail.findOne()
```

---

## 📊 Output Collections

### ⭐ `orders_detail`
- All enriched orders  
- Cleaned, transformed, and analytics-ready  

### ⭐ `city_metrics`
- Total revenue per city  
- Number of orders  
- Average order value  
- Average delivery rating  

### ⭐ `restaurant_metrics`
- Metrics grouped by both city and restaurant  
- Revenue, count, and ratings  

---

## 🌟 Why This Project Is Useful

This project is ideal for:
- Data Engineering learners  
- PySpark beginners  
- MongoDB integration practice  
- Portfolio / Resume building  
- End-to-end ETL pipeline demonstration  

It mirrors the structure of real production batch pipelines.

---

## 👨‍💻 Author

**Jat Rahul Singh**  
Data Engineering • Python • PySpark • MongoDB

---

## 📜 License  
This project is open source under the MIT License.
