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
      
    if basic_info:
        cols = st.columns(3)
        keys = list(basic_info.keys())

        for i in range(3):
            value = basic_info[keys[i]]
            cols[i].metric(label=keys[i], value=f"{value:}")
        else:
            st.warning("No basic info data available.")