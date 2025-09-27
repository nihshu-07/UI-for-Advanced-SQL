import streamlit as st
import pandas as pd

from db_functions import(
    connect_to_db,
    get_basic_info
)

st.sidebar.title("Inventory Management Dashboard")
option = st.sidebar.radio("Select Option :",["Basic Information","Operational Tasks"])

st.title('Inventory and Supply chain Dashboard')
db = connect_to_db()
cursor = db.cursor()

if option == "Basic Information":
    st.header("Basic Matrics")

    basic_info = get_basic_info(cursor)