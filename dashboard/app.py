import sqlite3
from pathlib import Path
import pandas as pd
import streamlit as st

base_dir = Path(__file__).resolve().parent.parent
db_path = base_dir / "database" / "usage_data.db"

st.title("SaaS Usage Intelligence Dashboard")


@st.cache_data
def load_data():
    """
    Load data from the SQLite database and return it as a DataFrame.
    """
    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query("SELECT * FROM usage_enriched", conn)
    conn.close()

    # Ensures the date column is datetime
    df["date"] = pd.to_datetime(df["date"])

    return df


df = load_data()

# Sidebar filters
st.sidebar.header("Filters")

company = st.sidebar.multiselect(
    "Company",
    sorted(df["company"].dropna().unique().tolist())
)

department = st.sidebar.multiselect(
    "Department",
    sorted(df["department"].dropna().unique().tolist())
)

min_date = df["date"].min().date()
max_date = df["date"].max().date()

date_range = st.sidebar.date_input(
    "Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

# Applying filters
filtered_df = df.copy()

if company:
    filtered_df = filtered_df[filtered_df["company"].isin(company)]

if department:
    filtered_df = filtered_df[filtered_df["department"].isin(department)]

# Date Range filtering
if isinstance(date_range, tuple) and len(date_range) == 2:
    start_date, end_date = date_range
    filtered_df = filtered_df[
        (filtered_df["date"].dt.date >= start_date) &
        (filtered_df["date"].dt.date <= end_date)
    ]

# Usage Metrics
st.subheader("Usage Metrics")
col1, col2, col3 = st.columns(3)

col1.metric("Total Users", filtered_df["user_id"].nunique())
col2.metric("Total Sessions", filtered_df["sessions"].sum())
col3.metric("Unique Applications", filtered_df["app"].nunique())

# Usage by application
st.subheader("Usage by Application")
app_usage = (
    filtered_df.groupby("app")["sessions"]
    .sum()
    .sort_values(ascending=False)
)

st.bar_chart(app_usage)

# Cost Metrics using filtered data
st.subheader("Estimated SaaS Spend by Application")

cost_by_app = (
    filtered_df.groupby("app")
    .agg(
        users=("user_id", "nunique"),
        seat_cost_usd=("seat_cost_usd", "max")
    )
)

cost_by_app["estimated_cost"] = cost_by_app["users"] * cost_by_app["seat_cost_usd"]
cost_by_app = cost_by_app["estimated_cost"].sort_values(ascending=False)

st.bar_chart(cost_by_app)

# Filtered Data Table
st.subheader("Usage Data")
st.dataframe(filtered_df.head())
