import pymysql

def connect_to_db():
    return pymysql.connect(
    host="localhost",
    user="root",
    password="ROOT",
    database="project_stream",
    port=3306)

def get_basic_info(cursor):
    queries = {
    "Total Suppliers":"SELECT COUNT(*) as total_suppliers FROM suppliers",
    
    "Total products": "SELECT count(*) as total_products FROM products",
    
    "Total category" :"SELECT count(distinct category) as total_category FROM products",
    
    "Total sales value made in last 3 months":"""SELECT ROUND(SUM(ABS(se.change_quantity) * p.price), 2) AS total_sales_last_3_months
    FROM stock_entries se
    JOIN products p 
    ON p.product_id = se.product_id
    WHERE se.change_type = 'Sale'
    AND se.entry_date >= (
        SELECT DATE_SUB(MAX(entry_date), INTERVAL 3 MONTH)
        FROM stock_entries)""",
    
    
    "Total restock value made in last 3 months":"""SELECT ROUND(SUM(ABS(se.change_quantity) * p.price), 2) AS total_restock_last_3_months
    FROM stock_entries se
    JOIN products p 
    ON p.product_id = se.product_id
    WHERE se.change_type = 'Restock'
    AND se.entry_date >= (
            SELECT DATE_SUB(MAX(entry_date), INTERVAL 3 MONTH)
            FROM stock_entries)""",
     
    "Below reorder and no pending reorders":"""SELECT COUNT(*) FROM products as p
    WHERE p.stock_quantity < p.reorder_level
    AND p.product_id NOT IN (
    SELECT DISTINCT product_id FROM reorders WHERE status = 'pending')"""	
    }

    result = {}
    for label, query in queries.items():
        cursor.execute(query)
        row = cursor.fetchone()
        result[label] = list(row)[0]

        return result 