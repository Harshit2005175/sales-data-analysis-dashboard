"""Functions for analyzing sales data and generating business insights."""

import pandas as pd


def get_total_revenue(dataframe):
    """Calculate the total revenue across all orders.
    
    Input: cleaned DataFrame with Revenue column
    Output: single float value (total revenue)
    """
    total = dataframe["Revenue"].sum()
    return round(total, 2)


def get_total_profit(dataframe):
    """Calculate the total profit across all orders.
    
    Input: cleaned DataFrame with Profit column
    Output: single float value (total profit)
    """
    total = dataframe["Profit"].sum()
    return round(total, 2)


def get_average_order_value(dataframe):
    """Calculate the average revenue per order.
    
    Input: cleaned DataFrame with Revenue column
    Output: single float value (average order value)
    """
    average = dataframe["Revenue"].mean()
    return round(average, 2)


def get_total_orders(dataframe):
    """Count the total number of orders.
    
    Input: cleaned DataFrame
    Output: single integer value (number of rows)
    """
    total = len(dataframe)
    return total


def get_best_selling_product(dataframe):
    """Find the product with the highest total revenue.
    
    Input: cleaned DataFrame with Product and Revenue columns
    Output: dictionary with product name and its total revenue
    
    Pandas concept used: groupby() to group by product
    """
    # Group by Product and sum the Revenue for each product
    product_revenue = dataframe.groupby("Product")["Revenue"].sum().sort_values(ascending=False)
    
    # Get the product with the highest revenue
    best_product = product_revenue.index[0]
    best_revenue = round(product_revenue.iloc[0], 2)
    
    return {"Product": best_product, "Revenue": best_revenue}


def get_worst_selling_product(dataframe):
    """Find the product with the lowest total revenue.
    
    Input: cleaned DataFrame with Product and Revenue columns
    Output: dictionary with product name and its total revenue
    
    Pandas concept used: groupby() to group by product
    """
    # Group by Product and sum the Revenue for each product
    product_revenue = dataframe.groupby("Product")["Revenue"].sum().sort_values(ascending=True)
    
    # Get the product with the lowest revenue
    worst_product = product_revenue.index[0]
    worst_revenue = round(product_revenue.iloc[0], 2)
    
    return {"Product": worst_product, "Revenue": worst_revenue}


def get_sales_by_category(dataframe):
    """Calculate total revenue for each product category.
    
    Input: cleaned DataFrame with Category and Revenue columns
    Output: pandas Series with categories as index and revenue as values
            (can be easily converted to dictionary or used in charts)
    
    Pandas concept used: groupby() and sum()
    """
    # Group by Category and sum the Revenue
    category_sales = dataframe.groupby("Category")["Revenue"].sum().sort_values(ascending=False)
    
    # Round all values to 2 decimal places
    category_sales = category_sales.round(2)
    
    return category_sales


def get_profit_by_category(dataframe):
    """Calculate total profit for each product category.
    
    Input: cleaned DataFrame with Category and Profit columns
    Output: pandas Series with categories as index and profit as values
    
    Pandas concept used: groupby() and sum()
    """
    # Group by Category and sum the Profit
    category_profit = dataframe.groupby("Category")["Profit"].sum().sort_values(ascending=False)
    
    # Round all values to 2 decimal places
    category_profit = category_profit.round(2)
    
    return category_profit


def get_monthly_sales(dataframe):
    """Calculate total revenue for each month.
    
    Input: cleaned DataFrame with Order_Date (datetime) and Revenue columns
    Output: pandas Series with months as index and revenue as values
    
    Pandas concept used: 
    - dt.to_period() to extract year-month from datetime
    - groupby() and sum()
    """
    # Extract year-month from the date column
    # dt.to_period('M') means "convert to monthly period"
    monthly_revenue = dataframe.groupby(dataframe["Order_Date"].dt.to_period("M"))["Revenue"].sum()
    
    # Round all values to 2 decimal places
    monthly_revenue = monthly_revenue.round(2)
    
    return monthly_revenue


def get_monthly_profit(dataframe):
    """Calculate total profit for each month.
    
    Input: cleaned DataFrame with Order_Date (datetime) and Profit columns
    Output: pandas Series with months as index and profit as values
    
    Pandas concept used:
    - dt.to_period() to extract year-month from datetime
    - groupby() and sum()
    """
    # Extract year-month from the date column
    monthly_profit = dataframe.groupby(dataframe["Order_Date"].dt.to_period("M"))["Profit"].sum()
    
    # Round all values to 2 decimal places
    monthly_profit = monthly_profit.round(2)
    
    return monthly_profit


def get_top_5_products_by_revenue(dataframe):
    """Find the top 5 products with the highest total revenue.
    
    Input: cleaned DataFrame with Product and Revenue columns
    Output: pandas DataFrame with products and their total revenue (sorted descending)
    
    Pandas concept used: groupby(), sum(), sort_values(), head()
    """
    # Group by Product and sum the Revenue
    product_revenue = dataframe.groupby("Product")["Revenue"].sum().sort_values(ascending=False)
    
    # Get top 5 products
    top_5 = product_revenue.head(5).round(2)
    
    # Convert to DataFrame for easier display in Streamlit
    top_5_df = top_5.reset_index()
    top_5_df.columns = ["Product", "Revenue"]
    
    return top_5_df


def get_top_5_products_by_profit(dataframe):
    """Find the top 5 products with the highest total profit.
    
    Input: cleaned DataFrame with Product and Profit columns
    Output: pandas DataFrame with products and their total profit (sorted descending)
    
    Pandas concept used: groupby(), sum(), sort_values(), head()
    """
    # Group by Product and sum the Profit
    product_profit = dataframe.groupby("Product")["Profit"].sum().sort_values(ascending=False)
    
    # Get top 5 products
    top_5 = product_profit.head(5).round(2)
    
    # Convert to DataFrame for easier display in Streamlit
    top_5_df = top_5.reset_index()
    top_5_df.columns = ["Product", "Profit"]
    
    return top_5_df


def get_all_metrics(dataframe):
    """Generate all key business metrics at once.
    
    Input: cleaned DataFrame
    Output: dictionary containing all metrics
    
    This function is useful for the Streamlit dashboard to get all data in one call.
    """
    metrics = {
        "Total Revenue": get_total_revenue(dataframe),
        "Total Profit": get_total_profit(dataframe),
        "Average Order Value": get_average_order_value(dataframe),
        "Total Orders": get_total_orders(dataframe),
        "Best Selling Product": get_best_selling_product(dataframe),
        "Worst Selling Product": get_worst_selling_product(dataframe),
        "Sales by Category": get_sales_by_category(dataframe),
        "Profit by Category": get_profit_by_category(dataframe),
        "Monthly Sales": get_monthly_sales(dataframe),
        "Monthly Profit": get_monthly_profit(dataframe),
        "Top 5 Products by Revenue": get_top_5_products_by_revenue(dataframe),
        "Top 5 Products by Profit": get_top_5_products_by_profit(dataframe),
    }
    return metrics


if __name__ == "__main__":
    # For testing: import the cleaned data
    from data_cleaning import load_and_clean_data
    
    cleaned_data = load_and_clean_data()
    
    print("\n--- Business Metrics ---")
    print(f"Total Revenue: ${get_total_revenue(cleaned_data)}")
    print(f"Total Profit: ${get_total_profit(cleaned_data)}")
    print(f"Average Order Value: ${get_average_order_value(cleaned_data)}")
    print(f"Total Orders: {get_total_orders(cleaned_data)}")
    print(f"\nBest Selling Product: {get_best_selling_product(cleaned_data)}")
    print(f"Worst Selling Product: {get_worst_selling_product(cleaned_data)}")
    
    print("\n--- Sales by Category ---")
    print(get_sales_by_category(cleaned_data))
    
    print("\n--- Top 5 Products by Revenue ---")
    print(get_top_5_products_by_revenue(cleaned_data))
    
    print("\n--- Top 5 Products by Profit ---")
    print(get_top_5_products_by_profit(cleaned_data))
