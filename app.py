import streamlit as st
import pandas as pd
import pymysql.cursors

from db_functions import(
    connect_to_db,
    get_basic_info
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
        