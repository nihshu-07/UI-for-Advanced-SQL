import streamlit as st
import pandas as pd

from db_functions import(
    connect_to_db,
    get_basic_info
)

st.sidebar.title("Inventory Management Dashboard")