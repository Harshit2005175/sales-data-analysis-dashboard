"""Streamlit dashboard for Sales Data Analysis."""

import streamlit as st
import pandas as pd
from datetime import datetime
import sys
from pathlib import Path

# Add the src directory to the path so we can import our modules
sys.path.insert(0, str(Path(__file__).parent / "src"))

from data_cleaning import load_and_clean_data
from analysis import (
    get_total_revenue,
    get_total_profit,
    get_total_orders,
    get_average_order_value,
    get_best_selling_product,
    get_worst_selling_product,
    get_sales_by_category,
    get_profit_by_category,
    get_monthly_sales,
    get_monthly_profit,
    get_top_5_products_by_revenue,
    get_top_5_products_by_profit,
)

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================
st.set_page_config(
    page_title="Sales Data Analysis Dashboard",
    page_icon="📊",
    layout="wide",
)

# ============================================================================
# TITLE AND DESCRIPTION
# ============================================================================
st.title("📊 Sales Data Analysis Dashboard")
st.markdown(
    """
    Welcome to the Sales Data Analysis Dashboard!
    
    This dashboard helps you analyze sales performance, track revenue and profit trends,
    and gain insights into your best-performing products and categories.
    """
)

# ============================================================================
# LOAD DATA (Only once, cached for performance)
# ============================================================================
@st.cache_data
def load_data():
    """Load and clean the sales data once when the app starts."""
    return load_and_clean_data()

with st.spinner("Loading and cleaning data..."):
    df = load_data()

st.success("✅ Data loaded successfully!")

# ============================================================================
# FILTERS SECTION
# ============================================================================
st.sidebar.header("🔍 Filters")

# Date range filter
min_date = df["Order_Date"].min().date()
max_date = df["Order_Date"].max().date()

date_range = st.sidebar.date_input(
    "Select Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date,
)

# Category filter
categories = ["All"] + sorted(df["Category"].unique().tolist())
selected_category = st.sidebar.selectbox("Select Category", categories)

# Product filter
if selected_category == "All":
    products = ["All"] + sorted(df["Product"].unique().tolist())
else:
    # If a category is selected, show only products in that category
    category_products = df[df["Category"] == selected_category]["Product"].unique()
    products = ["All"] + sorted(category_products.tolist())

selected_product = st.sidebar.selectbox("Select Product", products)

# ============================================================================
# APPLY FILTERS
# ============================================================================
# Filter by date range
filtered_df = df[
    (df["Order_Date"].dt.date >= date_range[0]) &
    (df["Order_Date"].dt.date <= date_range[1])
]

# Filter by category
if selected_category != "All":
    filtered_df = filtered_df[filtered_df["Category"] == selected_category]

# Filter by product
if selected_product != "All":
    filtered_df = filtered_df[filtered_df["Product"] == selected_product]

# ============================================================================
# KPI CARDS (KEY PERFORMANCE INDICATORS)
# ============================================================================
st.header("📈 Key Performance Indicators")

# Create 4 columns for KPI cards
col1, col2, col3, col4 = st.columns(4)

# Total Revenue KPI
with col1:
    total_revenue = get_total_revenue(filtered_df)
    st.metric(
        label="Total Revenue",
        value=f"${total_revenue:,.2f}",
        delta=None,
    )

# Total Profit KPI
with col2:
    total_profit = get_total_profit(filtered_df)
    st.metric(
        label="Total Profit",
        value=f"${total_profit:,.2f}",
        delta=None,
    )

# Total Orders KPI
with col3:
    total_orders = get_total_orders(filtered_df)
    st.metric(
        label="Total Orders",
        value=total_orders,
        delta=None,
    )

# Average Order Value KPI
with col4:
    avg_order_value = get_average_order_value(filtered_df)
    st.metric(
        label="Avg Order Value",
        value=f"${avg_order_value:,.2f}",
        delta=None,
    )

# ============================================================================
# CHARTS SECTION
# ============================================================================
st.header("📊 Sales Charts")

# Row 1: Monthly Sales and Monthly Profit
col1, col2 = st.columns(2)

with col1:
    st.subheader("Monthly Revenue Trend")
    monthly_sales = get_monthly_sales(filtered_df)
    if not monthly_sales.empty:
        # Convert index to string for better display
        monthly_sales_plot = monthly_sales.reset_index()
        monthly_sales_plot.columns = ["Month", "Revenue"]
        st.line_chart(
            data=monthly_sales_plot.set_index("Month"),
            height=300,
        )
    else:
        st.info("No data available for the selected filters.")

with col2:
    st.subheader("Monthly Profit Trend")
    monthly_profit = get_monthly_profit(filtered_df)
    if not monthly_profit.empty:
        # Convert index to string for better display
        monthly_profit_plot = monthly_profit.reset_index()
        monthly_profit_plot.columns = ["Month", "Profit"]
        st.line_chart(
            data=monthly_profit_plot.set_index("Month"),
            height=300,
        )
    else:
        st.info("No data available for the selected filters.")

# Row 2: Category Revenue and Category Profit
col1, col2 = st.columns(2)

with col1:
    st.subheader("Revenue by Category")
    category_sales = get_sales_by_category(filtered_df)
    if not category_sales.empty:
        st.bar_chart(category_sales)
    else:
        st.info("No data available for the selected filters.")

with col2:
    st.subheader("Profit by Category")
    category_profit = get_profit_by_category(filtered_df)
    if not category_profit.empty:
        st.bar_chart(category_profit)
    else:
        st.info("No data available for the selected filters.")

# ============================================================================
# TOP PRODUCTS SECTION
# ============================================================================
st.header("🏆 Top Performing Products")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Top 5 Products by Revenue")
    top_revenue = get_top_5_products_by_revenue(filtered_df)
    if not top_revenue.empty:
        # Display as a formatted table
        st.dataframe(
            top_revenue,
            use_container_width=True,
            hide_index=True,
        )
    else:
        st.info("No data available for the selected filters.")

with col2:
    st.subheader("Top 5 Products by Profit")
    top_profit = get_top_5_products_by_profit(filtered_df)
    if not top_profit.empty:
        # Display as a formatted table
        st.dataframe(
            top_profit,
            use_container_width=True,
            hide_index=True,
        )
    else:
        st.info("No data available for the selected filters.")

# ============================================================================
# FILTERED DATA TABLE
# ============================================================================
st.header("📋 Filtered Data Table")

# Select columns to display
display_columns = [
    "Order_ID",
    "Order_Date",
    "Region",
    "Product",
    "Category",
    "Quantity",
    "Unit_Price",
    "Revenue",
    "Profit",
    "Profit Margin",
]

# Only display columns that exist in the DataFrame
display_columns = [col for col in display_columns if col in filtered_df.columns]

# Display the table
st.dataframe(
    filtered_df[display_columns],
    use_container_width=True,
    hide_index=True,
)

# ============================================================================
# BUSINESS INSIGHTS SECTION
# ============================================================================
st.header("💡 Business Insights")

# Calculate insights based on filtered data
if len(filtered_df) > 0:
    col1, col2 = st.columns(2)
    
    with col1:
        # Best-selling product insight
        best_product = get_best_selling_product(filtered_df)
        st.info(
            f"🌟 **Best-selling Product**: {best_product['Product']}\n\n"
            f"Revenue: ${best_product['Revenue']:,.2f}"
        )
        
        # Profit margin insight
        avg_profit_margin = filtered_df["Profit Margin"].mean()
        st.info(
            f"📊 **Average Profit Margin**: {avg_profit_margin:.2f}%\n\n"
            f"This shows how much profit is earned from every dollar of revenue."
        )
    
    with col2:
        # Worst-selling product insight
        worst_product = get_worst_selling_product(filtered_df)
        st.warning(
            f"⚠️ **Lowest Revenue Product**: {worst_product['Product']}\n\n"
            f"Revenue: ${worst_product['Revenue']:,.2f}"
        )
        
        # Top category insight
        category_sales = get_sales_by_category(filtered_df)
        if not category_sales.empty:
            top_category = category_sales.index[0]
            top_category_revenue = category_sales.iloc[0]
            st.success(
                f"✅ **Top Category**: {top_category}\n\n"
                f"Revenue: ${top_category_revenue:,.2f}"
            )

else:
    st.warning("No data available for the selected filters. Please adjust your filters.")

# ============================================================================
# FOOTER
# ============================================================================
st.divider()
st.markdown(
    """
    ---
    **About this Dashboard**: This is a beginner-friendly Sales Data Analysis Dashboard
    built with Streamlit. It helps you understand sales trends and business performance.
    """
)
