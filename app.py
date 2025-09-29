import streamlit as st
import pandas as pd
import pymysql.cursors

from db_functions import(
    connect_to_db,
    get_basic_info,
    get_additional_tables,
    get_categories,
    get_suppliers,
    add_new_manual_id
)

st.sidebar.title("Inventory Management Dashboard")
option = st.sidebar.radio("Select Option :",["Basic Information","Operational Tasks"])

st.title('Inventory and Supply chain Dashboard')
db = connect_to_db()
cursor = db.cursor(pymysql.cursors.DictCursor)

if option == "Basic Information":
    st.header("Basic Metrics")

    basic_info = get_basic_info(cursor)
      
    cols = st.columns(3)
    keys = list(basic_info.keys())

    for i, key in enumerate(keys):
        cols[i % 3].metric(label=key, value=basic_info[key])
        

    tables = get_additional_tables(cursor)
    for labels,data in tables.items():
        st.header(labels)
        df = pd.DataFrame(data)
        st.dataframe(df)

if option ==  "Operational Tasks":
    st.header("Operaton Tasks")
    selected_task = st.selectbox("Choose an task",["Add new Product","Product History","Place Reorder","Recieve Reorder"])

    if selected_task == "Add new Product":
        st.header("Add New Product")
        categories = get_categories(cursor)
        suppliers = get_suppliers(cursor)

        with st.form("Add_Product_Form"):
            product_name = st.text_input("Product_name")
            product_category = st.selectbox("Category",categories)
            product_price = st.number_input("Price",min_value=0.00,step = 0.1)
            product_stock= st.number_input("Stock Quantity",min_value=0,step =1)
            product_level = st.number_input("Reorder level",min_value=0,step =1)

            supplier_ids=[s["supplier_id"] for s in suppliers]
            supplier_name=[s["supplier_name"] for s in suppliers]

            supplier_id = st.selectbox(
                "Supplier",
                options = supplier_ids,
                format_func = lambda x: supplier_name[supplier_ids.index(x)]
            )

            submitted = st.form_submit_button("Add Product")

            if submitted :
                if not product_name:
                    st.error("Please enter product name")
                else:
                    try:
                        add_new_manual_id(cursor,db,product_name,product_category,product_price
                                          ,product_stock,product_level,supplier_id)
                        st.success(f"Product {product_name} added successfully")
                    except Exception as e:
                        st.error(f"Error adding the product {e}")