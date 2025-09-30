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

def add_new_manual_id(cursor,db,p_name,p_category,p_price,p_stock,p_reorder,p_supplier):
    proc_call = "call AddNewProductManualId(%s,%s,%s,%s,%s,%s)"
    params = (p_name,p_category,p_price,p_stock,p_reorder,p_supplier)
    cursor.execute(proc_call,params)
    db.commit()

def get_categories(cursor):
    cursor.execute("SELECT DISTINCT category FROM products ORDER BY category ASC")
    rows = cursor.fetchall()
    return [row["category"]for row in rows]

def get_suppliers(cursor):
    cursor.execute("SELECT supplier_id , supplier_name FROM suppliers ORDER BY supplier_name ASC")
    return cursor.fetchall()

def get_all_products(cursor):
    cursor.execute("SELECT product_id,product_name FROM products ORDER BY product_name")
    return cursor.fetchall()

def get_product_history(cursor,product_id):
    query=("SELECT * FROM product_inventory_history WHERE product_id = %s ORDER BY record_date DESC")
    cursor.execute(query,(product_id,))
    return cursor.fetchall()

def place_reorder(cursor,db,product_id,reorder_quantity):
    query = """ 
            insert into reorders(reorder_id,product_id,reorder_quantity,reorder_date,status)
            select 
            max(reorder_id)+1,
            %s,
            %s,
            curdate(),
            "Ordered"
            from reorders;
            """
    cursor.execute(query,(product_id,reorder_quantity))
    db.commit()

def get_pending_reorders(cursor):
    cursor.execute("""
    select r.reorder_id,p.product_name from reorders as r join products as p on r.product_id = p.product_id
    """)
    return cursor.fetchall()

def mark_reorder_as_received(cursor,db,reorder_id):
    cursor.callproc("MarkReorderAsReceived",[reorder_id])
    db.commit()