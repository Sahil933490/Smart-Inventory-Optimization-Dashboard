import streamlit as st
import pandas as pd
import plotly.express as px
from src.database import get_connection, initialize_database
from src.queries import (
    get_kpis, get_category_summary, get_warehouse_revenue,
    get_monthly_revenue, get_top_products, get_stock_status,
    get_abc_summary, get_reorder_list
)

st.set_page_config(page_title="Smart Inventory Analytics", page_icon="📦", layout="wide")
st.title("📦 Smart Inventory Optimization & Demand Analytics")
st.caption("Python • SQL (SQLite) • Streamlit | Demonstration dataset: synthetic sales for 2025")

@st.cache_resource
def setup_db():
    conn = get_connection()
    initialize_database(conn)
    return conn

conn = setup_db()

# Sidebar filters
st.sidebar.header("Dashboard Filters")
categories = pd.read_sql_query("SELECT DISTINCT Category FROM inventory ORDER BY Category", conn)["Category"].tolist()
selected_categories = st.sidebar.multiselect("Category", categories, default=categories)
warehouses = pd.read_sql_query("SELECT DISTINCT Warehouse FROM inventory ORDER BY Warehouse", conn)["Warehouse"].tolist()
selected_warehouses = st.sidebar.multiselect("Warehouse", warehouses, default=warehouses)

# Parameterized filters are applied to the optimization/inventory summary.
cat_marks = ",".join(["?"] * len(selected_categories)) or "NULL"
wh_marks = ",".join(["?"] * len(selected_warehouses)) or "NULL"
where_sql = f"WHERE Category IN ({cat_marks}) AND Warehouse IN ({wh_marks})"
params = selected_categories + selected_warehouses

kpis = get_kpis(conn, where_sql, params)
c1,c2,c3,c4 = st.columns(4)
c1.metric("Inventory Value", f"₹{kpis['inventory_value']:,.0f}")
c2.metric("Products", f"{kpis['products']:,}")
c3.metric("Reorder Required", f"{kpis['reorder_required']:,}")
c4.metric("Critical Products", f"{kpis['critical_products']:,}")

st.divider()
left, right = st.columns(2)
with left:
    st.subheader("Inventory by Category")
    df = get_category_summary(conn, where_sql, params)
    if not df.empty:
        fig = px.bar(df, x="Category", y="Stock_Units", color="Category", title="Current stock units")
        st.plotly_chart(fig, use_container_width=True)
with right:
    st.subheader("ABC Classification")
    abc = get_abc_summary(conn, where_sql, params)
    if not abc.empty:
        fig = px.pie(abc, names="ABC_Category", values="Product_Count", hole=0.45,
                     title="Products by ABC class")
        st.plotly_chart(fig, use_container_width=True)

left, right = st.columns(2)
with left:
    st.subheader("Monthly Revenue Trend")
    monthly = get_monthly_revenue(conn, selected_warehouses)
    if not monthly.empty:
        fig = px.line(monthly, x="Month", y="Revenue", markers=True, title="Revenue by month")
        st.plotly_chart(fig, use_container_width=True)
with right:
    st.subheader("Warehouse Revenue")
    wh_rev = get_warehouse_revenue(conn, selected_warehouses)
    if not wh_rev.empty:
        fig = px.bar(wh_rev, x="Warehouse", y="Revenue", title="Revenue by warehouse")
        st.plotly_chart(fig, use_container_width=True)

st.divider()
st.subheader("Top 10 Products by Revenue")
top = get_top_products(conn, selected_warehouses)
st.dataframe(top, use_container_width=True, hide_index=True)

st.subheader("Products Requiring Replenishment")
reorder = get_reorder_list(conn, where_sql, params)
st.dataframe(reorder, use_container_width=True, hide_index=True)

with st.expander("Explore SQL outputs: stock status"):
    status = get_stock_status(conn, where_sql, params)
    st.dataframe(status, use_container_width=True, hide_index=True)

st.info("Note: This project uses synthetic demonstration data. EOQ, safety stock and reorder-point outputs depend on stated model assumptions; they are not live company recommendations.")
