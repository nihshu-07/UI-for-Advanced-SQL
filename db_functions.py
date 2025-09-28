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
    
    "Total sales value(last 3 months)":"""SELECT ROUND(SUM(ABS(se.change_quantity) * p.price), 2) AS total_sales_last_3_months
    FROM stock_entries se
    JOIN products p 
    ON p.product_id = se.product_id
    WHERE se.change_type = 'Sale'
    AND se.entry_date >= (
        SELECT DATE_SUB(MAX(entry_date), INTERVAL 3 MONTH)
        FROM stock_entries)""",
    
    
    "Total restock value(last 3 months)":"""SELECT ROUND(SUM(ABS(se.change_quantity) * p.price), 2) AS total_restock_last_3_months
    FROM stock_entries se
    JOIN products p 
    ON p.product_id = se.product_id
    WHERE se.change_type = 'Restock'
    AND se.entry_date >= (
            SELECT DATE_SUB(MAX(entry_date), INTERVAL 3 MONTH)
            FROM stock_entries)""",
     
    "Below & no pending reorders":"""SELECT COUNT(*) FROM products as p
    WHERE p.stock_quantity < p.reorder_level
    AND p.product_id NOT IN (
    SELECT DISTINCT product_id FROM reorders WHERE status = 'pending')"""	
    }

    result = {}
    for label, query in queries.items():
        cursor.execute(query)
        row = cursor.fetchone()

        if not row:  # No result returned
            result[label] = 0
        elif isinstance(row, dict):  # If using DictCursor
            # Get first value in dict
            result[label] = next(iter(row.values()))
        elif isinstance(row, (tuple, list)):  # If normal cursor
            result[label] = row[0]
        else:
            result[label] = row  # fallback

    return result 

def get_additional_tables(cursor):
    queries = {
        "Suppliers Contact details": "SELECT supplier_name,contact_name,email,phone FROM suppliers",

        "Product with supplier and stock": """SELECT p.product_name,s.supplier_name,p.stock_quantity,p.reorder_level 
                                            FROM products as p
                                            JOIN suppliers s ON
                                            p.supplier_id = s.supplier_id
                                            ORDER BY p.product_name ASC""",

        "Product needing reorder": """SELECT product_id,product_name,stock_quantity,reorder_level FROM products
                                    WHERE stock_quantity < reorder_level;"""
    }

    tables = {}
    for label, query in queries.items():
        cursor.execute(query)
        tables[label] = cursor.fetchall()

    return tables