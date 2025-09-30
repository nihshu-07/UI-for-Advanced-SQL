# INVENTORY MANAGEMENT DASHBOARD (UI for advanced SQL)

A streamlined Streamlit based user interface for executing **advanced SQL queries on MySQL databases**  without writing queries manually every time.  
Ideal for analysts, engineers, or business users who want **quick access to prebuilt SQL analytics through a clean web dashboard.**

---

## ✨ Features

- 🔌 Connects directly to **MySQL**
- 📦 Execute **predefined complex SQL queries** with one click
- 📊 View results in **structured tables / metrics**
- 🧮 Supports **aggregations, joins, date filtering** (e.g., last 3 months)
- 🧱 Modular structure — easily **add or modify queries in `db_functions.py`**
- 🌐 Runs locally via **Streamlit web UI**

---

## 🧱 Tech Stack

| Component | Technology |
|-----------|------------|
| UI        | Streamlit |
| Backend   | Python |
| Database  | MySQL |
| Connector | `pymysql` |
| Data Handling | `pandas` |

---

## 🗃️ Dataset

The Dataset used in this project is there in the repo itself with the name Data.

---

## ⚙️ Setup & Installation

```bash
  # 1. Clone repository
  git clone https://github.com/nihshu-07/UI-for-Advanced-SQL.git
  cd UI-for-Advanced-SQL
  
  # 2. (Optional) Create a virtual environment
  python -m venv venv
  venv\Scripts\activate  # on Windows
  # source venv/bin/activate  # on macOS/Linux
  
  # 3. Install dependencies
  pip install -r requirements.txt
```
---

## 🔐 Database Configuration

Before running the app, configure your MySQL credentials.

Update your database connection in db_functions.py (or use environment variables):

DB_HOST = "localhost"
DB_USER = "your_username"
DB_PASSWORD = "your_password"
DB_NAME = "your_database"

---

## 🚀 Run the Application
```bash
streamlit run app.py
```
Then open the UI at:

👉 http://localhost:8501

---

## 🖱️ How to Use

- Open the application in your browser

- Select a query or metric category from the sidebar

- The backend runs the corresponding SQL query automatically

- Results are displayed as metrics or tables

  ---

## 🧩 Extending / Adding New SQL Queries

To add more functionality:

- Open db_functions.py

- Add a new entry to the queries dictionary

- The UI will automatically pick it up

  ---

## 📸 Screenshots


<img width="1903" height="899" alt="image" src="https://github.com/user-attachments/assets/59ea59fe-cc0c-449a-9361-517f2ea06805" />

<img width="1913" height="846" alt="image" src="https://github.com/user-attachments/assets/7062d56d-b075-4518-8b34-7fa0715c46e6" />


---

## 🛤️ Roadmap / Future Improvements

✅ Export results as CSV / Excel

✅ Support for custom query input

✅ Add user authentication

❌ Multi-database support (PostgreSQL, SQLite, etc.)

----

