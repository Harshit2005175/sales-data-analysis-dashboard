"""Reusable charts for the Sales Data Analysis Dashboard."""

import matplotlib.pyplot as plt
import seaborn as sns


# Use a simple, consistent style for every chart in the project.
sns.set_theme(style="whitegrid")


def plot_monthly_revenue(monthly_revenue):
    """Create a line chart showing revenue for each month.

    Input:
        monthly_revenue: pandas Series returned by analysis.get_monthly_sales()

    Returns:
        A matplotlib Figure that can be displayed with Streamlit.
    """
    figure, axis = plt.subplots(figsize=(10, 5))

    # Convert the PeriodIndex to text so month labels display clearly.
    months = monthly_revenue.index.astype(str)
    axis.plot(months, monthly_revenue.values, marker="o", color="royalblue")

    axis.set_title("Monthly Revenue Trend")
    axis.set_xlabel("Month")
    axis.set_ylabel("Revenue")
    axis.tick_params(axis="x", rotation=45)
    figure.tight_layout()

    return figure


def plot_monthly_profit(monthly_profit):
    """Create a line chart showing profit for each month.

    Input:
        monthly_profit: pandas Series returned by analysis.get_monthly_profit()

    Returns:
        A matplotlib Figure that can be displayed with Streamlit.
    """
    figure, axis = plt.subplots(figsize=(10, 5))

    months = monthly_profit.index.astype(str)
    axis.plot(months, monthly_profit.values, marker="o", color="seagreen")

    axis.set_title("Monthly Profit Trend")
    axis.set_xlabel("Month")
    axis.set_ylabel("Profit")
    axis.tick_params(axis="x", rotation=45)
    figure.tight_layout()

    return figure


def plot_revenue_by_category(category_revenue):
    """Create a bar chart showing revenue for each category.

    Input:
        category_revenue: pandas Series returned by
            analysis.get_sales_by_category()

    Returns:
        A matplotlib Figure that can be displayed with Streamlit.
    """
    figure, axis = plt.subplots(figsize=(8, 5))

    # A Series can be passed directly to seaborn after resetting its index.
    chart_data = category_revenue.reset_index()
    chart_data.columns = ["Category", "Revenue"]
    sns.barplot(data=chart_data, x="Category", y="Revenue", ax=axis, color="cornflowerblue")

    axis.set_title("Revenue by Category")
    axis.set_xlabel("Category")
    axis.set_ylabel("Revenue")
    axis.tick_params(axis="x", rotation=30)
    figure.tight_layout()

    return figure


def plot_profit_by_category(category_profit):
    """Create a bar chart showing profit for each category.

    Input:
        category_profit: pandas Series returned by
            analysis.get_profit_by_category()

    Returns:
        A matplotlib Figure that can be displayed with Streamlit.
    """
    figure, axis = plt.subplots(figsize=(8, 5))

    chart_data = category_profit.reset_index()
    chart_data.columns = ["Category", "Profit"]
    sns.barplot(data=chart_data, x="Category", y="Profit", ax=axis, color="mediumseagreen")

    axis.set_title("Profit by Category")
    axis.set_xlabel("Category")
    axis.set_ylabel("Profit")
    axis.tick_params(axis="x", rotation=30)
    figure.tight_layout()

    return figure


def plot_top_5_products_by_revenue(top_products):
    """Create a bar chart for the top five products by revenue.

    Input:
        top_products: DataFrame returned by
            analysis.get_top_5_products_by_revenue()

    Returns:
        A matplotlib Figure that can be displayed with Streamlit.
    """
    figure, axis = plt.subplots(figsize=(9, 5))

    sns.barplot(
        data=top_products,
        x="Revenue",
        y="Product",
        ax=axis,
        color="darkorange",
    )

    axis.set_title("Top 5 Products by Revenue")
    axis.set_xlabel("Revenue")
    axis.set_ylabel("Product")
    figure.tight_layout()

    return figure


def plot_top_5_products_by_profit(top_products):
    """Create a bar chart for the top five products by profit.

    Input:
        top_products: DataFrame returned by
            analysis.get_top_5_products_by_profit()

    Returns:
        A matplotlib Figure that can be displayed with Streamlit.
    """
    figure, axis = plt.subplots(figsize=(9, 5))

    sns.barplot(
        data=top_products,
        x="Profit",
        y="Product",
        ax=axis,
        color="purple",
    )

    axis.set_title("Top 5 Products by Profit")
    axis.set_xlabel("Profit")
    axis.set_ylabel("Product")
    figure.tight_layout()

    return figure
