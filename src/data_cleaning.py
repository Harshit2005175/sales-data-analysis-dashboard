"""Functions for loading, inspecting, and cleaning the sales dataset."""

from pathlib import Path

import pandas as pd


# Build the file path from this file's location so the code works from any folder.
DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "sales_data.csv"


def inspect_data(dataframe):
    """Print a beginner-friendly summary of the input DataFrame."""
    print("\n--- Dataset inspection ---")
    print(f"Number of rows: {dataframe.shape[0]}")
    print(f"Number of columns: {dataframe.shape[1]}")
    print(f"Column names: {list(dataframe.columns)}")
    print("\nData types:")
    print(dataframe.dtypes)
    print("\nMissing values in each column:")
    print(dataframe.isnull().sum())
    print(f"\nDuplicate rows: {dataframe.duplicated().sum()}")


def clean_data(dataframe):
    """Clean sales data and add the columns used for analysis."""
    cleaned_data = dataframe.copy()

    # Remove completely repeated records. Keep the first occurrence.
    cleaned_data = cleaned_data.drop_duplicates().copy()

    # Convert dates. Invalid dates become NaT (missing datetime values).
    cleaned_data["Order_Date"] = pd.to_datetime(
        cleaned_data["Order_Date"], errors="coerce"
    )

    # Convert columns that should contain numbers. Invalid text becomes NaN.
    numeric_columns = ["Quantity", "Unit_Price", "Cost_Price"]
    for column in numeric_columns:
        cleaned_data[column] = pd.to_numeric(cleaned_data[column], errors="coerce")

    # A row without a valid date cannot be used in monthly analysis, so remove it.
    cleaned_data = cleaned_data.dropna(subset=["Order_Date"]).copy()

    # Fill missing numeric values with that column's median.
    # Median is less affected by unusually large or small values than the mean.
    for column in numeric_columns:
        if cleaned_data[column].isnull().any():
            cleaned_data[column] = cleaned_data[column].fillna(
                cleaned_data[column].median()
            )

    # Fill missing text values with a clear label instead of deleting the sale.
    text_columns = ["Region", "Product", "Category", "Customer_Name", "Salesperson"]
    for column in text_columns:
        cleaned_data[column] = cleaned_data[column].fillna("Unknown")

    # Calculate business metrics after cleaning the input columns.
    cleaned_data["Revenue"] = cleaned_data["Quantity"] * cleaned_data["Unit_Price"]
    cleaned_data["Profit"] = cleaned_data["Revenue"] - (
        cleaned_data["Quantity"] * cleaned_data["Cost_Price"]
    )
    cleaned_data["Profit Margin"] = (
        cleaned_data["Profit"] / cleaned_data["Revenue"] * 100
    ).round(2)

    # Replace an undefined margin (for example, if Revenue is zero) with 0.
    cleaned_data["Profit Margin"] = cleaned_data["Profit Margin"].fillna(0)

    return cleaned_data.reset_index(drop=True)


def load_and_clean_data(file_path=DATA_FILE):
    """Read the CSV, show its original state, clean it, and return the result."""
    sales_data = pd.read_csv(file_path)
    inspect_data(sales_data)
    cleaned_data = clean_data(sales_data)

    print("\n--- After cleaning ---")
    print(f"Number of rows: {cleaned_data.shape[0]}")
    print(f"Number of columns: {cleaned_data.shape[1]}")
    print(f"Remaining missing values: {cleaned_data.isnull().sum().sum()}")
    print(f"Remaining duplicate rows: {cleaned_data.duplicated().sum()}")

    return cleaned_data


if __name__ == "__main__":
    cleaned_sales_data = load_and_clean_data()
    print("\nFirst five cleaned records:")
    print(cleaned_sales_data.head())
